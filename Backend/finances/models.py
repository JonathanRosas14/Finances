from django.db import models

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
        
    def __str__(self):
        return self.username