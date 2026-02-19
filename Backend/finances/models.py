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
    
