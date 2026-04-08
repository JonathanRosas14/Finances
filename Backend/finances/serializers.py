from rest_framework import serializers
from .models import User, Category, Transaction, Budget, Goal, Debt
from django.db.models import Sum
import re


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        min_length=3,
        max_length=50,
        error_messages={
            'min_length': 'El username debe tener al menos 3 caracteres.',
            'max_length': 'El username no puede tener más de 50 caracteres.',
            'required': 'El username es obligatorio.',
        }
    )
    email = serializers.EmailField(
        max_length=100,
        error_messages={
            'invalid': 'Ingresa un email válido.',
            'required': 'El email es obligatorio.',
        }
    )
    password = serializers.CharField(
        min_length=8,
        max_length=255,
        error_messages={
            'min_length': 'La contraseña debe tener al menos 8 caracteres.',
            'required': 'La contraseña es obligatoria.',
        }
    )

    def validate_username(self, value):
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                'El username solo puede contener letras, números y guiones bajos.'
            )
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Este username ya está en uso.'
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Este email ya está registrado.'
            )
        return value.lower()

    def validate_password(self, value):
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError(
                'La contraseña debe tener al menos una letra mayúscula.'
            )
        if not re.search(r'\d', value):
            raise serializers.ValidationError(
                'La contraseña debe tener al menos un número.'
            )
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        error_messages={
            'invalid': 'Ingresa un email válido.',
            'required': 'El email es obligatorio.',
        }
    )
    password = serializers.CharField(
        error_messages={
            'required': 'La contraseña es obligatoria.',
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
            raise serializers.ValidationError('Ya existe una categoría con ese nombre')
        
        return value
            
class TransactionSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(required=False, allow_null=True, write_only=False)
    category_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'transaction_date', 'description', 'category_id', 'category_name', 'type', 'payment_method', 'is_recurring', 'recurring_frequency', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at', 'category_name']
    
    def get_category_name(self, obj):
        return obj.category.name if obj.category else 'Sin categoría'
    
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
                raise serializers.ValidationError('Categoría no encontrada')
        
        return Transaction.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        category_id = validated_data.pop('category_id', None)
        
        if category_id is not None:
            if category_id:
                try:
                    category = Category.objects.get(id=category_id, user=self.context['request'].user)
                    instance.category = category
                except Category.DoesNotExist:
                    raise serializers.ValidationError('Categoría no encontrada')
            else:
                instance.category = None
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
    
    def validate_transaction_date(self, value):
        if value is None:
            raise serializers.ValidationError('La fecha es obligatoria')
        return value
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('El monto debe ser mayor a 0')
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
            raise serializers.ValidationError('El monto del presupuesto debe ser mayor a 0')
        return value
    
    def validate(self, data):
        if data.get('end_date') and data.get('start_date'):
            if data['end_date'] < data['start_date']:
                raise serializers.ValidationError('La fecha de fin debe ser posterior a la fecha de inicio')
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

class DebtSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField(read_only=True)
    paid_amount_calculated = serializers.SerializerMethodField(read_only=True)
    remaining_amount = serializers.SerializerMethodField(read_only=True)
    total_with_interest = serializers.SerializerMethodField(read_only=True)
    progress_percentage = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Debt
        fields = [
            'id',
            'name',
            'category',
            'category_name',
            'creditor',
            'total_amount',
            'paid_amount',
            'paid_amount_calculated',
            'remaining_amount',
            'total_with_interest',
            'progress_percentage',
            'due_date',
            'interest_rate',
            'months',
            'description',
            'status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'category_name', 'paid_amount_calculated', 'remaining_amount', 'total_with_interest', 'progress_percentage']

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    
    def get_total_with_interest(self, obj):
        """Calcula el total con intereses incluidos"""
        try:
            total = float(obj.total_amount)
            rate = float(obj.interest_rate)
            months = int(obj.months) or 1
            
            interest = total * (rate / 100) * months
            total_with_interest = total + interest
            
            return round(total_with_interest, 2)
        except Exception as e:
            print(f"Error calculando total_with_interest para debt {obj.id}: {e}")
            return round(float(obj.total_amount), 2)
    
    def get_paid_amount_calculated(self, obj):
        """Calcula el monto pagado sumando transacciones de gastos de esa categoría"""
        if not obj.category:
            return 0.0
        
        try:
            total = Transaction.objects.filter(
                user=obj.user,
                category=obj.category,
                type='expense'
            ).aggregate(Sum('amount'))['amount__sum']
            
            if total is None:
                return 0.0
            
            return round(float(total), 2)
        except Exception as e:
            print(f"Error calculando paid_amount para debt {obj.id}: {e}")
            return 0.0
    
    def get_remaining_amount(self, obj):
        """Calcula el monto pendiente"""
        try:
            total_with_interest = self.get_total_with_interest(obj)
            paid = self.get_paid_amount_calculated(obj)
            remaining = total_with_interest - paid
            return round(max(remaining, 0), 2)
        except Exception as e:
            print(f"Error calculando remaining_amount para debt {obj.id}: {e}")
            return 0.0
    
    def get_progress_percentage(self, obj):
        """Calcula el porcentaje de progreso"""
        try:
            total_with_interest = self.get_total_with_interest(obj)
            if total_with_interest == 0:
                return 0.0
            
            paid = self.get_paid_amount_calculated(obj)
            progress = (paid / total_with_interest) * 100
            return round(min(progress, 100), 2)
        except Exception as e:
            print(f"Error calculando progress_percentage para debt {obj.id}: {e}")
            return 0.0
    
    def validate_total_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('El monto total debe ser mayor que cero')
        return value
    
    def validate_paid_amount(self, value):
        if value < 0:
            raise serializers.ValidationError('El monto pagado no puede ser negativo')
        return value
    
    def validate_months(self, value):
        if value < 1:
            raise serializers.ValidationError('Los meses deben ser al menos 1')
        return value
    
    def validate(self, data):
        total = data.get('total_amount', 0)
        paid = data.get('paid_amount', 0)
        
        if self.instance:
            total = data.get('total_amount', self.instance.total_amount)
            paid = data.get('paid_amount', self.instance.paid_amount)
        
        if paid > total:
            raise serializers.ValidationError('El monto pagado no puede ser mayor al monto total')
        
        return data