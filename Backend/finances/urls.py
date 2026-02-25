from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('google/', views.google_auth, name='google_auth'),
    path('categories/', views.get_categories, name='get_categories'),
    path('categories/create/', views.create_category, name='create_category'),
    path('categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    path('categories/<int:category_id>/', views.update_category, name='update_category'),
    path('transactions/', views.get_transactions, name='get_transactions'),
    path('transactions/create/', views.create_transaction, name='create_transaction'),
    path('transactions/<int:transaction_id>/delete/', views.delete_transaction, name='delete_transaction'),
    path('transactions/<int:transaction_id>/', views.update_transaction, name='update_transaction'),
]