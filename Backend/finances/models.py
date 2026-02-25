from django.db import models
import bcrypt

class User(models.Model):
    PROVIDER_CHOICES = [
        ('local', 'Local'),
        ('google', 'Google'),
        ('apple', 'Apple'),
    ]
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128)
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default='local')
    provider_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
    
    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True
    
    @property
    def is_active(self):
        """Return True if the user is active."""
        return True
    
    def set_password(self, raw_password):
        self.password = bcrypt.hashpw(
            raw_password.encode('utf-8'), 
            bcrypt.gensalt()
        ).decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.checkpw(
            raw_password.encode('utf-8'), 
            self.password.encode('utf-8')
        )    
        
    def __str__(self):
        return self.username

class Category(models.Model):
    Type_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, default='📦')
    color = models.CharField(max_length=7, default='#95A5A6')
    type = models.CharField(max_length=20, choices=Type_CHOICES)
    parent_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categories'
        unique_together = ('user', 'name', 'type')
    
    def __str__(self):
        return f"{self.name} ({self.type})"
    
class Transaction(models.Model):
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField()
    description = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='expense')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash')
    is_recurring = models.BooleanField(default=False)
    recurring_frequency = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transactions'
        ordering = ['-transaction_date']
    
    def __str__(self):
        cat_name = self.category.name if self.category else 'Sin categoría'
        return f"{cat_name}: {self.amount} on {self.transaction_date}"
