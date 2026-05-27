from django.urls import path, re_path
from . import views

urlpatterns = [
    # ── AUTH ─────────────────────────────────────────────────────
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('google/', views.google_auth, name='google_auth'),

    # ── CATEGORIES ───────────────────────────────────────────────
    re_path(r'^categories/?$', views.get_categories, name='get_categories'),
    path('categories/create/', views.create_category, name='create_category'),
    re_path(r'^categories/(?P<category_id>\d+)/?$', views.update_category, name='update_category'),
    re_path(r'^categories/(?P<category_id>\d+)/delete/?$', views.delete_category, name='delete_category'),

    # ── TRANSACTIONS ─────────────────────────────────────────────
    re_path(r'^transactions/?$', views.get_transactions, name='get_transactions'),
    path('transactions/create/', views.create_transaction, name='create_transaction'),
    re_path(r'^transactions/(?P<transaction_id>\d+)/?$', views.update_transaction, name='update_transaction'),
    re_path(r'^transactions/(?P<transaction_id>\d+)/delete/?$', views.delete_transaction, name='delete_transaction'),

    # ── BUDGETS ──────────────────────────────────────────────────
    re_path(r'^budgets/?$', views.get_budgets, name='get_budgets'),
    path('budgets/create/', views.create_budget, name='create_budget'),
    re_path(r'^budgets/(?P<budget_id>\d+)/?$', views.update_budget, name='update_budget'),
    re_path(r'^budgets/(?P<budget_id>\d+)/delete/?$', views.delete_budget, name='delete_budget'),

    # ── GOALS ────────────────────────────────────────────────────
    re_path(r'^goals/?$', views.get_goals, name='get_goals'),
    path('goals/create/', views.create_goal, name='create_goal'),
    re_path(r'^goals/(?P<goal_id>\d+)/?$', views.update_goal, name='update_goal'),
    re_path(r'^goals/(?P<goal_id>\d+)/delete/?$', views.delete_goal, name='delete_goal'),

    # ── DEBTS ────────────────────────────────────────────────────
    re_path(r'^debts/?$', views.get_debts, name='get_debts'),
    path('debts/create/', views.create_debt, name='create_debt'),
    re_path(r'^debts/(?P<debt_id>\d+)/?$', views.update_debt, name='update_debt'),
    re_path(r'^debts/(?P<debt_id>\d+)/delete/?$', views.delete_debt, name='delete_debt'),
]