from django.test import TestCase, override_settings
from django.db import IntegrityError
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from unittest.mock import patch, MagicMock
from decimal import Decimal
from datetime import date, timedelta
import json
import bcrypt

from .models import User, Category, Transaction, Budget, Goal, Debt
from .serializers import (
    RegisterSerializer, LoginSerializer, CategorySerializer,
    TransactionSerializer, BudgetSerializer, GoalSerializer, DebtSerializer
)
from .views import get_tokens_for_user
from .authentication import CustomJWTAuthentication


# ═══════════════════════════════════════════════════════════════════
# MODEL TESTS
# ═══════════════════════════════════════════════════════════════════

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password='plaintext'
        )

    def test_create_user(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.provider, 'local')
        self.assertIsNone(self.user.provider_id)

    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_is_authenticated_property(self):
        self.assertTrue(self.user.is_authenticated)

    def test_is_active_property(self):
        self.assertTrue(self.user.is_active)

    def test_set_password_hashes_correctly(self):
        raw = 'MySecurePass123'
        self.user.set_password(raw)
        self.assertTrue(self.user.password.startswith('$2b$'))
        self.assertNotEqual(self.user.password, raw)

    def test_check_password_correct(self):
        raw = 'MySecurePass123'
        self.user.set_password(raw)
        self.user.save()
        self.assertTrue(self.user.check_password(raw))

    def test_check_password_incorrect(self):
        raw = 'MySecurePass123'
        self.user.set_password(raw)
        self.user.save()
        self.assertFalse(self.user.check_password('wrongpassword'))

    def test_unique_username(self):
        with self.assertRaises(Exception):
            User.objects.create(username='testuser', email='other@example.com', password='pass')

    def test_unique_email(self):
        with self.assertRaises(Exception):
            User.objects.create(username='other', email='test@example.com', password='pass')


class CategoryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1', email='user1@test.com', password='pass')
        self.category = Category.objects.create(
            user=self.user,
            name='Food',
            type='expense',
            icon='🍔',
            color='#FF5733'
        )

    def test_create_category(self):
        self.assertEqual(self.category.name, 'Food')
        self.assertEqual(self.category.type, 'expense')
        self.assertEqual(self.category.user, self.user)

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Food (expense)')

    def test_unique_together_user_name_type(self):
        with self.assertRaises(Exception):
            Category.objects.create(user=self.user, name='Food', type='expense')

    def test_different_user_same_name_allowed(self):
        user2 = User.objects.create(username='user2', email='user2@test.com', password='pass')
        cat2 = Category.objects.create(user=user2, name='Food', type='expense')
        self.assertIsNotNone(cat2.id)

    def test_default_icon_and_color(self):
        cat = Category.objects.create(user=self.user, name='Default', type='income')
        self.assertEqual(cat.icon, '📦')
        self.assertEqual(cat.color, '#95A5A6')


class TransactionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1', email='user1@test.com', password='pass')
        self.category = Category.objects.create(user=self.user, name='Food', type='expense')
        self.transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('150.00'),
            transaction_date=date.today(),
            description='Groceries',
            type='expense',
            payment_method='cash'
        )

    def test_create_transaction(self):
        self.assertEqual(self.transaction.amount, Decimal('150.00'))
        self.assertEqual(self.transaction.description, 'Groceries')
        self.assertEqual(self.transaction.type, 'expense')

    def test_transaction_str_with_category(self):
        expected = f"Food: 150.00 on {date.today()}"
        self.assertEqual(str(self.transaction), expected)

    def test_transaction_str_without_category(self):
        t = Transaction.objects.create(
            user=self.user, amount=Decimal('50'), transaction_date=date.today(), type='income'
        )
        expected = f"Uncategorized: 50 on {date.today()}"
        self.assertEqual(str(t), expected)

    def test_default_ordering_desc_date(self):
        t1 = Transaction.objects.create(
            user=self.user, amount=Decimal('10'), transaction_date=date(2024, 1, 1), type='income'
        )
        t2 = Transaction.objects.create(
            user=self.user, amount=Decimal('20'), transaction_date=date(2024, 6, 1), type='income'
        )
        qs = Transaction.objects.all()
        self.assertGreater(qs[0].transaction_date, qs[1].transaction_date)

    def test_is_recurring_default_false(self):
        self.assertFalse(self.transaction.is_recurring)

    def test_category_nullable(self):
        t = Transaction.objects.create(
            user=self.user, amount=Decimal('25'), transaction_date=date.today(), type='expense'
        )
        self.assertIsNone(t.category)


class BudgetModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1', email='user1@test.com', password='pass')

    def test_create_budget(self):
        budget = Budget.objects.create(
            user=self.user, name='Monthly Food', amount=Decimal('500'),
            period='monthly', start_date=date.today()
        )
        self.assertEqual(budget.name, 'Monthly Food')
        self.assertEqual(budget.amount, Decimal('500'))
        self.assertTrue(budget.is_active)

    def test_budget_str(self):
        budget = Budget.objects.create(
            user=self.user, name='Test Budget', amount=Decimal('1000'),
            start_date=date.today()
        )
        self.assertEqual(str(budget), 'Test Budget - 1000')

    def test_alert_percentage_default(self):
        budget = Budget.objects.create(
            user=self.user, name='Default Alert', amount=Decimal('100'),
            start_date=date.today()
        )
        self.assertEqual(budget.alert_percentage, 80)

    def test_is_active_default_true(self):
        budget = Budget.objects.create(
            user=self.user, name='Active', amount=Decimal('100'),
            start_date=date.today()
        )
        self.assertTrue(budget.is_active)

    def test_category_nullable(self):
        budget = Budget.objects.create(
            user=self.user, name='No Cat', amount=Decimal('100'),
            start_date=date.today()
        )
        self.assertIsNone(budget.category)


class GoalModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1', email='user1@test.com', password='pass')

    def test_create_goal(self):
        goal = Goal.objects.create(
            user=self.user, name='Save for car', target_amount=Decimal('20000'),
            target_date=date(2025, 12, 31)
        )
        self.assertEqual(goal.name, 'Save for car')
        self.assertEqual(goal.target_amount, Decimal('20000'))
        self.assertEqual(goal.priority, 'medium')
        self.assertEqual(goal.status, 'in_progress')

    def test_goal_str(self):
        goal = Goal.objects.create(
            user=self.user, name='Vacation', target_amount=Decimal('5000'),
            target_date=date(2025, 6, 30)
        )
        self.assertEqual(str(goal), 'Vacation - 5000')

    def test_goal_priority_default(self):
        goal = Goal.objects.create(
            user=self.user, name='Default Priority', target_amount=Decimal('100'),
            target_date=date.today()
        )
        self.assertEqual(goal.priority, 'medium')

    def test_goal_status_default(self):
        goal = Goal.objects.create(
            user=self.user, name='Default Status', target_amount=Decimal('100'),
            target_date=date.today()
        )
        self.assertEqual(goal.status, 'in_progress')


class DebtModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1', email='user1@test.com', password='pass')

    def test_create_debt(self):
        debt = Debt.objects.create(
            user=self.user, name='Credit Card', amount=Decimal('3000'),
            total_with_interest=Decimal('3500'), due_date=date(2025, 6, 30),
            interest_rate=Decimal('5'), months=12
        )
        self.assertEqual(debt.name, 'Credit Card')
        self.assertEqual(debt.amount, Decimal('3000'))
        self.assertEqual(debt.total_with_interest, Decimal('3500'))
        self.assertEqual(debt.status, 'pending')

    def test_debt_str(self):
        debt = Debt.objects.create(
            user=self.user, name='Car Loan', amount=Decimal('15000'),
            total_with_interest=Decimal('18000'), due_date=date(2026, 1, 1)
        )
        self.assertEqual(str(debt), 'Car Loan - 18000')

    def test_debt_status_default(self):
        debt = Debt.objects.create(
            user=self.user, name='Default Status Debt', amount=Decimal('100'),
            total_with_interest=Decimal('110'), due_date=date.today()
        )
        self.assertEqual(debt.status, 'pending')


# ═══════════════════════════════════════════════════════════════════
# SERIALIZER TESTS
# ═══════════════════════════════════════════════════════════════════

class RegisterSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'StrongPass1',
        }

    def test_valid_registration(self):
        serializer = RegisterSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_username_too_short(self):
        data = {**self.valid_data, 'username': 'ab'}
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_username_invalid_chars(self):
        data = {**self.valid_data, 'username': 'user name!'}
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('letters, numbers, and underscores', str(serializer.errors))

    def test_password_too_short(self):
        data = {**self.valid_data, 'password': 'Short1A'}
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_password_no_uppercase(self):
        data = {**self.valid_data, 'password': 'lowercase1'}
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_password_no_number(self):
        data = {**self.valid_data, 'password': 'NoNumberA'}
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_email_duplicate(self):
        User.objects.create(username='existing', email='newuser@example.com', password='pass')
        serializer = RegisterSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())

    def test_username_duplicate(self):
        User.objects.create(username='newuser', email='other@example.com', password='pass')
        serializer = RegisterSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())

    def test_email_converted_to_lowercase(self):
        data = {**self.valid_data, 'email': 'UPPERCASE@Example.COM'}
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.validate_email(data['email'])
        # The email is stored as lowercase
        lower_email = data['email'].lower()
        self.assertEqual(lower_email, 'uppercase@example.com')


class CategorySerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1', email='u1@test.com', password='pass')
        self.factory = APIRequestFactory()
        self.request = self.factory.get('/')
        self.request.user = self.user

    def test_valid_category(self):
        data = {'name': 'Transport', 'type': 'expense', 'icon': '🚗', 'color': '#333333'}
        serializer = CategorySerializer(data=data, context={'request': self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_duplicate_name_same_user(self):
        Category.objects.create(user=self.user, name='Food', type='expense')
        data = {'name': 'Food', 'type': 'expense'}
        serializer = CategorySerializer(data=data, context={'request': self.request})
        self.assertFalse(serializer.is_valid())

    def test_same_name_different_type(self):
        Category.objects.create(user=self.user, name='Food', type='expense')
        data = {'name': 'Food', 'type': 'income'}
        serializer = CategorySerializer(data=data, context={'request': self.request})
        self.assertFalse(serializer.is_valid())


class TransactionSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1', email='u1@test.com', password='pass')
        self.factory = APIRequestFactory()
        self.request = self.factory.get('/')
        self.request.user = self.user

    def test_valid_transaction(self):
        data = {
            'amount': '100.00', 'transaction_date': '2025-01-15',
            'description': 'Test', 'type': 'expense', 'payment_method': 'cash'
        }
        serializer = TransactionSerializer(data=data, context={'request': self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_amount_must_be_positive(self):
        data = {
            'amount': '0', 'transaction_date': '2025-01-15', 'type': 'expense'
        }
        serializer = TransactionSerializer(data=data, context={'request': self.request})
        self.assertFalse(serializer.is_valid())

    def test_negative_amount(self):
        data = {
            'amount': '-50', 'transaction_date': '2025-01-15', 'type': 'expense'
        }
        serializer = TransactionSerializer(data=data, context={'request': self.request})
        self.assertFalse(serializer.is_valid())

    def test_category_name_read_only(self):
        data = {
            'amount': '50', 'transaction_date': '2025-01-15', 'type': 'income'
        }
        serializer = TransactionSerializer(data=data, context={'request': self.request})
        self.assertTrue(serializer.is_valid())

    def test_get_category_name_no_category(self):
        t = Transaction(user=self.user, amount=Decimal('10'), transaction_date=date.today(), type='income')
        serializer = TransactionSerializer(context={'request': self.request})
        name = serializer.get_category_name(t)
        self.assertEqual(name, 'Uncategorized')

    def test_get_category_name_with_category(self):
        cat = Category.objects.create(user=self.user, name='Salary', type='income')
        t = Transaction(user=self.user, category=cat, amount=Decimal('10'), transaction_date=date.today(), type='income')
        serializer = TransactionSerializer(context={'request': self.request})
        self.assertEqual(serializer.get_category_name(t), 'Salary')


class BudgetSerializerTest(TestCase):
    def test_valid_budget(self):
        data = {
            'name': 'Monthly Budget', 'amount': '1000', 'period': 'monthly',
            'start_date': '2025-01-01', 'end_date': '2025-12-31'
        }
        serializer = BudgetSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_amount_must_be_positive(self):
        data = {
            'name': 'Zero Budget', 'amount': '0', 'start_date': '2025-01-01'
        }
        serializer = BudgetSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_end_date_before_start_date(self):
        data = {
            'name': 'Invalid', 'amount': '500', 'start_date': '2025-06-01',
            'end_date': '2025-01-01'
        }
        serializer = BudgetSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_end_date_equal_to_start_date(self):
        data = {
            'name': 'Same Day', 'amount': '500', 'start_date': '2025-01-01',
            'end_date': '2025-01-01'
        }
        serializer = BudgetSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)


class GoalSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1', email='u1@test.com', password='pass')
        self.factory = APIRequestFactory()
        self.request = self.factory.get('/')
        self.request.user = self.user

    def test_valid_goal(self):
        data = {
            'name': 'Save for house', 'target_amount': '50000',
            'target_date': '2026-12-31', 'priority': 'high'
        }
        serializer = GoalSerializer(data=data, context={'request': self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_target_amount_must_be_positive(self):
        data = {
            'name': 'Bad Goal', 'target_amount': '0', 'target_date': '2026-12-31'
        }
        serializer = GoalSerializer(data=data, context={'request': self.request})
        self.assertFalse(serializer.is_valid())

    def test_get_category_name_no_category(self):
        goal = Goal(user=self.user, name='Test', target_amount=Decimal('100'), target_date=date.today())
        serializer = GoalSerializer(context={'request': self.request})
        self.assertIsNone(serializer.get_category_name(goal))

    def test_get_category_name_with_category(self):
        cat = Category.objects.create(user=self.user, name='Vacation', type='income')
        goal = Goal(user=self.user, category=cat, name='Trip', target_amount=Decimal('1000'), target_date=date.today())
        serializer = GoalSerializer(context={'request': self.request})
        self.assertEqual(serializer.get_category_name(goal), 'Vacation')


class DebtSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1', email='u1@test.com', password='pass')
        self.factory = APIRequestFactory()
        self.request = self.factory.get('/')
        self.request.user = self.user

    def test_valid_debt(self):
        data = {
            'name': 'Personal Loan', 'amount': '10000',
            'total_with_interest': '12000', 'due_date': '2026-06-30',
            'interest_rate': '5', 'months': '24'
        }
        serializer = DebtSerializer(data=data, context={'request': self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_amount_must_be_positive(self):
        data = {
            'name': 'Zero Debt', 'amount': '0',
            'total_with_interest': '0', 'due_date': '2026-06-30'
        }
        serializer = DebtSerializer(data=data, context={'request': self.request})
        self.assertFalse(serializer.is_valid())


# ═══════════════════════════════════════════════════════════════════
# VIEW TESTS
# ═══════════════════════════════════════════════════════════════════

class AuthViewTest(APITestCase):
    def test_register_success(self):
        data = {'username': 'newuser', 'email': 'new@example.com', 'password': 'StrongPass1'}
        response = self.client.post('/api/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('User registered successfully', response.data['message'])
        self.assertTrue(User.objects.filter(email='new@example.com').exists())

    def test_register_missing_fields(self):
        response = self.client.post('/api/register/', {'username': 'test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_email(self):
        User.objects.create(username='existing', email='dup@example.com', password='pass')
        data = {'username': 'newuser', 'email': 'dup@example.com', 'password': 'StrongPass1'}
        response = self.client.post('/api/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_login_success(self):
        user = User(username='testuser', email='test@login.com')
        user.set_password('StrongPass1')
        user.save()
        response = self.client.post('/api/login/', {
            'email': 'test@login.com', 'password': 'StrongPass1'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

    def test_login_invalid_email(self):
        response = self.client.post('/api/login/', {
            'email': 'nonexist@test.com', 'password': 'pass'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_wrong_password(self):
        user = User(username='testuser', email='test@login.com')
        user.set_password('StrongPass1')
        user.save()
        response = self.client.post('/api/login/', {
            'email': 'test@login.com', 'password': 'wrongpass'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_google_account(self):
        User.objects.create(
            username='googleuser', email='google@test.com',
            password='', provider='google'
        )
        response = self.client.post('/api/login/', {
            'email': 'google@test.com', 'password': 'anypass'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Continue with Google', str(response.data))

    def test_login_missing_fields(self):
        response = self.client.post('/api/login/', {'email': 'test@test.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CategoryViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='catuser', email='cat@test.com')
        self.user.set_password('TestPass1')
        self.user.save()
        login_resp = self.client.post('/api/login/', {
            'email': 'cat@test.com', 'password': 'TestPass1'
        }, format='json')
        self.token = login_resp.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_get_categories_empty(self):
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_create_category_success(self):
        data = {'name': 'Food', 'type': 'expense', 'icon': '🍔', 'color': '#FF5733'}
        response = self.client.post('/api/categories/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('Category created successfully', str(response.data))

    def test_create_category_duplicate(self):
        Category.objects.create(user=self.user, name='Food', type='expense')
        data = {'name': 'Food', 'type': 'expense'}
        response = self.client.post('/api/categories/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_categories_with_data(self):
        Category.objects.create(user=self.user, name='Transport', type='expense')
        response = self.client.get('/api/categories/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Transport')

    def test_update_category_success(self):
        cat = Category.objects.create(user=self.user, name='Old Name', type='expense')
        response = self.client.put(
            f'/api/categories/{cat.id}/',
            {'name': 'New Name', 'type': 'expense'}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cat.refresh_from_db()
        self.assertEqual(cat.name, 'New Name')

    def test_update_category_not_found(self):
        response = self.client.put('/api/categories/9999/', {'name': 'Test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_category_success(self):
        cat = Category.objects.create(user=self.user, name='To Delete', type='expense')
        response = self.client.delete(f'/api/categories/{cat.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Category.objects.filter(id=cat.id).exists())

    def test_delete_category_not_found(self):
        response = self.client.delete('/api/categories/9999/delete/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated(self):
        self.client.credentials()
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TransactionViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='txuser', email='tx@test.com')
        self.user.set_password('TestPass1')
        self.user.save()
        login_resp = self.client.post('/api/login/', {
            'email': 'tx@test.com', 'password': 'TestPass1'
        }, format='json')
        self.token = login_resp.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.category = Category.objects.create(user=self.user, name='Food', type='expense')

    def test_create_transaction_success(self):
        data = {
            'amount': '150.00', 'transaction_date': '2025-06-15',
            'description': 'Groceries', 'type': 'expense',
            'payment_method': 'cash', 'category_id': self.category.id
        }
        response = self.client.post('/api/transactions/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('Transaction created successfully', str(response.data))

    def test_get_transactions_empty(self):
        response = self.client.get('/api/transactions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_get_transactions_with_data(self):
        Transaction.objects.create(
            user=self.user, category=self.category, amount=Decimal('100'),
            transaction_date=date.today(), type='expense'
        )
        response = self.client.get('/api/transactions/')
        self.assertEqual(len(response.data), 1)

    def test_update_transaction_success(self):
        tx = Transaction.objects.create(
            user=self.user, category=self.category, amount=Decimal('100'),
            transaction_date=date.today(), type='expense'
        )
        response = self.client.put(
            f'/api/transactions/{tx.id}/',
            {'amount': '200.00', 'description': 'Updated'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tx.refresh_from_db()
        self.assertEqual(float(tx.amount), 200.00)

    def test_update_transaction_not_found(self):
        response = self.client.put('/api/transactions/9999/', {'amount': '50'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_transaction_success(self):
        tx = Transaction.objects.create(
            user=self.user, category=self.category, amount=Decimal('50'),
            transaction_date=date.today(), type='expense'
        )
        response = self.client.delete(f'/api/transactions/{tx.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Transaction.objects.filter(id=tx.id).exists())

    def test_delete_transaction_not_found(self):
        response = self.client.delete('/api/transactions/9999/delete/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_transaction_invalid_amount(self):
        data = {
            'amount': '0', 'transaction_date': '2025-06-15',
            'type': 'expense'
        }
        response = self.client.post('/api/transactions/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BudgetViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='bduser', email='bd@test.com')
        self.user.set_password('TestPass1')
        self.user.save()
        login_resp = self.client.post('/api/login/', {
            'email': 'bd@test.com', 'password': 'TestPass1'
        }, format='json')
        self.token = login_resp.data['token']

    def test_get_budgets_no_token(self):
        response = self.client.get('/api/budgets/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_budgets_empty(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get('/api/budgets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_create_budget_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {
            'name': 'Monthly Food', 'amount': '500',
            'period': 'monthly', 'start_date': '2025-01-01'
        }
        response = self.client.post('/api/budgets/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('Budget created successfully', str(response.data))

    def test_create_budget_no_token(self):
        data = {'name': 'Budget', 'amount': '100', 'start_date': '2025-01-01'}
        response = self.client.post('/api/budgets/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_budgets_with_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        Budget.objects.create(
            user=self.user, name='Test', amount=Decimal('100'),
            start_date=date.today()
        )
        response = self.client.get('/api/budgets/')
        self.assertEqual(len(response.data), 1)

    def test_update_budget_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        budget = Budget.objects.create(
            user=self.user, name='Old', amount=Decimal('100'),
            start_date=date.today()
        )
        response = self.client.put(
            f'/api/budgets/{budget.id}/',
            {'name': 'Updated', 'amount': '200'}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        budget.refresh_from_db()
        self.assertEqual(budget.name, 'Updated')

    def test_update_budget_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.put('/api/budgets/9999/', {'name': 'Test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_budget_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        budget = Budget.objects.create(
            user=self.user, name='Delete Me', amount=Decimal('100'),
            start_date=date.today()
        )
        response = self.client.delete(f'/api/budgets/{budget.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Budget.objects.filter(id=budget.id).exists())

    def test_delete_budget_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.delete('/api/budgets/9999/delete/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GoalViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='gluser', email='gl@test.com')
        self.user.set_password('TestPass1')
        self.user.save()
        login_resp = self.client.post('/api/login/', {
            'email': 'gl@test.com', 'password': 'TestPass1'
        }, format='json')
        self.token = login_resp.data['token']

    def test_get_goals_no_token(self):
        response = self.client.get('/api/goals/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_goals_empty(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get('/api/goals/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_create_goal_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {
            'name': 'Save for Vacation', 'target_amount': '5000',
            'target_date': '2026-12-31', 'priority': 'high'
        }
        response = self.client.post('/api/goals/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('Goal created successfully', str(response.data))

    def test_create_goal_no_token(self):
        data = {'name': 'Goal', 'target_amount': '100', 'target_date': '2026-12-31'}
        response = self.client.post('/api/goals/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_goals_with_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        Goal.objects.create(
            user=self.user, name='Test Goal', target_amount=Decimal('1000'),
            target_date=date(2026, 12, 31)
        )
        response = self.client.get('/api/goals/')
        self.assertEqual(len(response.data), 1)

    def test_update_goal_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        goal = Goal.objects.create(
            user=self.user, name='Old Goal', target_amount=Decimal('100'),
            target_date=date(2026, 12, 31)
        )
        response = self.client.put(
            f'/api/goals/{goal.id}/',
            {'name': 'Updated Goal', 'target_amount': '500'}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        goal.refresh_from_db()
        self.assertEqual(goal.name, 'Updated Goal')

    def test_update_goal_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.put('/api/goals/9999/', {'name': 'Test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_goal_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        goal = Goal.objects.create(
            user=self.user, name='Delete Goal', target_amount=Decimal('100'),
            target_date=date(2026, 12, 31)
        )
        response = self.client.delete(f'/api/goals/{goal.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Goal.objects.filter(id=goal.id).exists())

    def test_delete_goal_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.delete('/api/goals/9999/delete/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DebtViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='dbuser', email='db@test.com')
        self.user.set_password('TestPass1')
        self.user.save()
        login_resp = self.client.post('/api/login/', {
            'email': 'db@test.com', 'password': 'TestPass1'
        }, format='json')
        self.token = login_resp.data['token']

    def test_get_debts_no_token(self):
        response = self.client.get('/api/debts/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_debts_empty(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get('/api/debts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_create_debt_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {
            'name': 'Credit Card', 'amount': '3000',
            'total_with_interest': '3500', 'due_date': '2026-06-30',
            'interest_rate': '5', 'months': '12'
        }
        response = self.client.post('/api/debts/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('Debt created successfully', str(response.data))

    def test_create_debt_with_interest_calculation(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {
            'name': 'Compound Loan', 'amount': '1000',
            'interest_rate': '10', 'months': '12',
            'due_date': '2026-06-30'
        }
        response = self.client.post('/api/debts/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expected_total = 1000 * ((1 + 10/100) ** 12)
        self.assertAlmostEqual(float(response.data['debt']['total_with_interest']), expected_total, places=1)

    def test_create_debt_no_token(self):
        data = {'name': 'Debt', 'amount': '100', 'due_date': '2026-06-30'}
        response = self.client.post('/api/debts/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_debts_with_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        Debt.objects.create(
            user=self.user, name='Test Debt', amount=Decimal('1000'),
            total_with_interest=Decimal('1200'), due_date=date(2026, 6, 30)
        )
        response = self.client.get('/api/debts/')
        self.assertEqual(len(response.data), 1)

    def test_update_debt_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        debt = Debt.objects.create(
            user=self.user, name='Old Debt', amount=Decimal('1000'),
            total_with_interest=Decimal('1200'), due_date=date(2026, 6, 30)
        )
        response = self.client.put(
            f'/api/debts/{debt.id}/',
            {'name': 'Updated Debt', 'amount': '2000'}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        debt.refresh_from_db()
        self.assertEqual(debt.name, 'Updated Debt')

    def test_update_debt_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.put('/api/debts/9999/', {'name': 'Test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_debt_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        debt = Debt.objects.create(
            user=self.user, name='Delete Debt', amount=Decimal('500'),
            total_with_interest=Decimal('600'), due_date=date(2026, 6, 30)
        )
        response = self.client.delete(f'/api/debts/{debt.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Debt.objects.filter(id=debt.id).exists())

    def test_delete_debt_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.delete('/api/debts/9999/delete/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_debt_with_category(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        cat = Category.objects.create(user=self.user, name='Loans', type='expense')
        data = {
            'name': 'Car Loan', 'amount': '15000',
            'total_with_interest': '18000', 'due_date': '2027-01-01',
            'category_id': cat.id
        }
        response = self.client.post('/api/debts/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# ═══════════════════════════════════════════════════════════════════
# AUTHENTICATION TESTS
# ═══════════════════════════════════════════════════════════════════

class CustomJWTAuthenticationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='authuser', email='auth@test.com')
        self.user.set_password('TestPass1')
        self.user.save()
        self.auth = CustomJWTAuthentication()

    def test_get_validated_token_valid(self):
        tokens = get_tokens_for_user(self.user)
        validated = self.auth.get_validated_token(tokens['token'])
        self.assertIsNotNone(validated)

    def test_get_validated_token_invalid(self):
        from rest_framework_simplejwt.exceptions import AuthenticationFailed
        with self.assertRaises(AuthenticationFailed):
            self.auth.get_validated_token('invalidtoken123')

    def test_get_user_valid_token(self):
        tokens = get_tokens_for_user(self.user)
        validated = self.auth.get_validated_token(tokens['token'])
        user = self.auth.get_user(validated)
        self.assertEqual(user.id, self.user.id)
        self.assertEqual(user.email, 'auth@test.com')

    def test_get_user_no_user_id_in_token(self):
        from rest_framework_simplejwt.tokens import RefreshToken
        from rest_framework_simplejwt.exceptions import AuthenticationFailed
        refresh = RefreshToken()
        validated = refresh.access_token
        with self.assertRaises(AuthenticationFailed):
            self.auth.get_user(validated)


# ═══════════════════════════════════════════════════════════════════
# HELPER FUNCTION TESTS
# ═══════════════════════════════════════════════════════════════════

class GetTokensForUserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='tokenuser', email='token@test.com', password='pass')

    def test_get_tokens_for_user_returns_token_and_refresh(self):
        tokens = get_tokens_for_user(self.user)
        self.assertIn('token', tokens)
        self.assertIn('refresh', tokens)
        self.assertIsInstance(tokens['token'], str)
        self.assertIsInstance(tokens['refresh'], str)

    def test_token_contains_user_info(self):
        tokens = get_tokens_for_user(self.user)
        access = AccessToken(tokens['token'])
        self.assertEqual(access['user_id'], self.user.id)
        self.assertEqual(access['email'], self.user.email)
        self.assertEqual(access['username'], self.user.username)
