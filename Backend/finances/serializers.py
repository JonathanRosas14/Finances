from rest_framework import serializers
from .models import User, Category, Transaction
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