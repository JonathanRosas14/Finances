from django.urls import path
from . import views

urlpatterns = [
    # ── AUTH ─────────────────────────────────────────────────────
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('google/', views.google_auth, name='google_auth'),

    # ── CATEGORIES ───────────────────────────────────────────────
    path('categories/', views.get_categories, name='get_categories'),
    path('categories/create/', views.create_category, name='create_category'),
    path('categories/<int:category_id>/', views.update_category, name='update_category'),
    path('categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),

    # ── TRANSACTIONS ─────────────────────────────────────────────
    path('transactions/', views.get_transactions, name='get_transactions'),
    path('transactions/create/', views.create_transaction, name='create_transaction'),
    path('transactions/<int:transaction_id>/', views.update_transaction, name='update_transaction'),
    path('transactions/<int:transaction_id>/delete/', views.delete_transaction, name='delete_transaction'),

    # ── BUDGETS ──────────────────────────────────────────────────
    path('budgets/', views.get_budgets, name='get_budgets'),
    path('budgets/create/', views.create_budget, name='create_budget'),
    path('budgets/<int:budget_id>/', views.update_budget, name='update_budget'),
    path('budgets/<int:budget_id>/delete/', views.delete_budget, name='delete_budget'),

    # ── GOALS ────────────────────────────────────────────────────
    path('goals/', views.get_goals, name='get_goals'),
    path('goals/create/', views.create_goal, name='create_goal'),
    path('goals/<int:goal_id>/', views.update_goal, name='update_goal'),
    path('goals/<int:goal_id>/delete/', views.delete_goal, name='delete_goal'),

    # ── DEBTS ────────────────────────────────────────────────────
    path('debts/', views.get_debts, name='get_debts'),
    path('debts/create/', views.create_debt, name='create_debt'),
    path('debts/<int:debt_id>/', views.update_debt, name='update_debt'),
    path('debts/<int:debt_id>/delete/', views.delete_debt, name='delete_debt'),
]