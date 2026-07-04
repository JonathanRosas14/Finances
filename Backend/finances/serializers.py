from rest_framework import serializers
from .models import User, Category, Transaction, Budget, Goal, Debt
import re


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        min_length=3,
        max_length=50,
        error_messages={
            'min_length': 'Username must be at least 3 characters.',
            'max_length': 'Username cannot exceed 50 characters.',
            'required': 'Username is required.',
        }
    )
    email = serializers.EmailField(
        max_length=100,
        error_messages={
            'invalid': 'Enter a valid email.',
            'required': 'Email is required.',
        }
    )
    password = serializers.CharField(
        min_length=8,
        max_length=255,
        error_messages={
            'min_length': 'Password must be at least 8 characters.',
            'required': 'Password is required.',
        }
    )

    def validate_username(self, value):
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                'Username can only contain letters, numbers, and underscores.'
            )
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'This username is already taken.'
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'This email is already registered.'
            )
        return value.lower()

    def validate_password(self, value):
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError(
                'Password must have at least one uppercase letter.'
            )
        if not re.search(r'\d', value):
            raise serializers.ValidationError(
                'Password must have at least one number.'
            )
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        error_messages={
            'invalid': 'Enter a valid email.',
            'required': 'Email is required.',
        }
    )
    password = serializers.CharField(
        error_messages={
            'required': 'Password is required.',
        }
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'provider', 'created_at']
        read_only_fields = ['id', 'created_at']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'color', 'type', 'parent_id', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_name(self, value):
        user = self.context['request'].user
        category_id = self.instance.id if self.instance else None
        
        query = Category.objects.filter(user=user, name=value)
        if category_id:
            query = query.exclude(id=category_id)
        
        if query.exists():
            raise serializers.ValidationError('A category with that name already exists')
        
        return value


class TransactionSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(required=False, allow_null=True, write_only=False)
    category_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'transaction_date', 'description', 'category_id', 'category_name', 'type', 'payment_method', 'is_recurring', 'recurring_frequency', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at', 'category_name']
    
    def get_category_name(self, obj):
        return obj.category.name if obj.category else 'Uncategorized'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category_id'] = instance.category.id if instance.category else None
        return data
    
    def create(self, validated_data):
        category_id = validated_data.pop('category_id', None)
        
        if category_id:
            try:
                category = Category.objects.get(id=category_id, user=self.context['request'].user)
                validated_data['category'] = category
            except Category.DoesNotExist:
                raise serializers.ValidationError('Category not found')
        
        return Transaction.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        category_id = validated_data.pop('category_id', None)
        
        if category_id is not None:
            if category_id:
                try:
                    category = Category.objects.get(id=category_id, user=self.context['request'].user)
                    instance.category = category
                except Category.DoesNotExist:
                    raise serializers.ValidationError('Category not found')
            else:
                instance.category = None
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
    
    def validate_transaction_date(self, value):
        if value is None:
            raise serializers.ValidationError('Date is required')
        return value
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Amount must be greater than 0')
        return value


class BudgetSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Budget
        fields = [
            'id', 
            'name', 
            'category', 
            'category_name',
            'amount', 
            'period', 
            'start_date', 
            'end_date', 
            'alert_percentage',
            'is_active',
            'description',
            'created_at'
        ]  
    read_only_fields = ['id', 'created_at', 'category_name']

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Budget amount must be greater than 0')
        return value
    
    def validate(self, data):
        if data.get('end_date') and data.get('start_date'):
            if data['end_date'] < data['start_date']:
                raise serializers.ValidationError('End date must be after start date')
        return data
    
# Gersson le toca esto
class GoalSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField(read_only=True)
    current_amount = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Goal
        fields = [
            'id', 
            'name', 
            'category',
            'category_name',
            'description',
            'target_amount', 
            'target_date', 
            'priority',
            'status',
            'current_amount',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'category_name', 'current_amount']
    
    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    
    def get_current_amount(self, obj):
        """Calcula el monto actual basado en transacciones de ingresos de la categoría asociada"""
        if not obj.category:
            return 0.0
        
        try:
            total = Transaction.objects.filter(
                user=obj.user,
                category=obj.category, 
                type='income'
            ).aggregate(Sum('amount'))['amount__sum']
            
            if total is None:
                return 0.0
            return float(total)
        except Exception as e:
            print(f"Error calculando current_amount para goal {obj.id}: {e}")
            return 0.0
    
    def validate_target_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('El monto objetivo debe ser mayor que cero')
        return value
    
    def validate_target_date(self, value):
        from datetime import date
        if value < date.today():
            raise serializers.ValidationError('La fecha objetivo no puede ser en el pasado')
        return value


class GoalSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField(read_only=True)
    category_id   = serializers.IntegerField(required=False, allow_null=True, write_only=False)

    class Meta:
        model = Goal
        fields = [
            'id',
            'name',
            'description',
            'target_amount',
            'target_date',
            'category_id',
            'category_name',
            'priority',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'category_name']

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category_id'] = instance.category.id if instance.category else None
        return data

    def validate_target_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Target amount must be greater than 0')
        return value


class DebtSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField(read_only=True)
    category_id   = serializers.IntegerField(required=False, allow_null=True, write_only=False)

    class Meta:
        model = Debt
        fields = [
            'id',
            'name',
            'creditor_name',
            'amount',
            'interest_rate',
            'months',
            'total_with_interest',
            'due_date',
            'category_id',
            'category_name',
            'description',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'category_name']

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category_id'] = instance.category.id if instance.category else None
        return data

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Amount must be greater than 0')
        return value