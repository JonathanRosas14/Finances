from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from .serializers import RegisterSerializer, LoginSerializer, CategorySerializer, TransactionSerializer, BudgetSerializer, GoalSerializer, DebtSerializer
from .models import User, Category, Transaction, Budget, Goal, Debt
import bcrypt
import os


def get_tokens_for_user(user):
    refresh = RefreshToken()
    refresh['user_id'] = user.id
    refresh['id'] = user.id
    refresh['email'] = user.email
    refresh['username'] = user.username
    access = refresh.access_token
    return {
        'token': str(access),
        'refresh': str(refresh),
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response(
                {'message': 'Todos los campos son obligatorios'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {'message': 'El usuario ya existe'},
                status=status.HTTP_409_CONFLICT
            )

        hashed = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        user = User(username=username, email=email, password=hashed)
        user.save()

        return Response(
            {'message': 'Usuario registrado exitosamente'},
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
        print(f"Error en register: {e}")
        return Response(
            {'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'message': 'Todos los campos son obligatorios'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'message': 'Credenciales inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.password and user.provider == 'google':
            return Response(
                {'message': "Esta cuenta fue creada con Google. Usa 'Continuar con Google'."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not bcrypt.checkpw(
            password.encode('utf-8'),
            user.password.encode('utf-8')
        ):
            return Response(
                {'message': 'Credenciales inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        tokens = get_tokens_for_user(user)
        return Response({
            'token': tokens['token'],
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        })
    except Exception as e:
        print(f"Error en login: {e}")
        return Response(
            {'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def google_auth(request):
    try:
        google_token = request.data.get('token')

        idinfo = id_token.verify_oauth2_token(
            google_token,
            google_requests.Request(),
            os.environ.get('GOOGLE_CLIENT_ID')
        )

        email = idinfo['email']
        username = idinfo.get('name', email.split('@')[0])
        provider_id = idinfo['sub']

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': username,
                'provider': 'google',
                'provider_id': provider_id,
            }
        )

        tokens = get_tokens_for_user(user)
        return Response({
            'token': tokens['token'],
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'isNewUser': created
        })
    except Exception as e:
        print(f"Error en google_auth: {e}")
        return Response(
            {'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ── CATEGORIES ───────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_categories(request):
    try:
        categories = Category.objects.filter(user=request.user).order_by('-created_at')
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(f"Error en get_categories: {e}")
        return Response(
            {'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_category(request):
    try:
        serializer = CategorySerializer(data=request.data, context={'request': request})
        
        if not serializer.is_valid():
            errors = serializer.errors
            first_error = next(iter(errors.values()))[0]
            return Response(
                {'message': str(first_error)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        category = serializer.save(user=request.user)
        
        return Response({
            'message': 'Categoría creada exitosamente',
            'category': CategorySerializer(category).data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print(f"Error en create_category: {e}")
        return Response(
            {'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_category(request, category_id):
    try:
        try:
            category = Category.objects.get(id=category_id, user=request.user)
        except Category.DoesNotExist:
            return Response(
                {'message': 'Categoría no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = CategorySerializer(category, data=request.data, context={'request': request})
        
        if not serializer.is_valid():
            errors = serializer.errors
            first_error = next(iter(errors.values()))[0]
            return Response(
                {'message': str(first_error)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()
        
        return Response({'message': 'Categoría actualizada exitosamente'})
        
    except Exception as e:
        print(f"Error en update_category: {e}")
        return Response(
            {'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_category(request, category_id):
    try:
        try:
            category = Category.objects.get(id=category_id, user=request.user)
        except Category.DoesNotExist:
            return Response(
                {'message': 'Categoría no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        category.delete()
        
        return Response({'message': 'Categoría eliminada exitosamente'})
        
    except Exception as e:
        print(f"Error en delete_category: {e}")
        return Response(
            {'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ── TRANSACTIONS ─────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transactions(request):
    try:
        transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
        serializer = TransactionSerializer(transactions, many=True, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        print(f"Error en get_transactions: {e}")
        return Response(
            {'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_transaction(request):
    try:
        serializer = TransactionSerializer(data=request.data, context={'request': request})
        
        if not serializer.is_valid():
            errors = serializer.errors
            first_error = next(iter(errors.values()))[0]
            return Response(
                {'message': str(first_error)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        transaction = serializer.save(user=request.user)
        
        return Response({
            'message': 'Transacción creada exitosamente',
            'transaction': TransactionSerializer(transaction, context={'request': request}).data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print(f"Error en create_transaction: {e}")
        return Response(
            {'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_transaction(request, transaction_id):
    try:
        try:
            transaction = Transaction.objects.get(id=transaction_id, user=request.user)
        except Transaction.DoesNotExist:
            return Response(
                {'message': 'Transacción no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = TransactionSerializer(transaction, data=request.data, context={'request': request}, partial=True)
        
        if not serializer.is_valid():
            errors = serializer.errors
            first_error = next(iter(errors.values()))[0]
            return Response(
                {'message': str(first_error)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()
        
        return Response({
            'message': 'Transacción actualizada exitosamente',
            'transaction': TransactionSerializer(serializer.instance, context={'request': request}).data
        })
        
    except Exception as e:
        print(f"Error en update_transaction: {e}")
        return Response(
            {'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_transaction(request, transaction_id):
    try:
        try:
            transaction = Transaction.objects.get(id=transaction_id, user=request.user)
        except Transaction.DoesNotExist:
            return Response(
                {'message': 'Transacción no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        transaction.delete()
        
        return Response({'message': 'Transacción eliminada exitosamente'})
        
    except Exception as e:
        print(f"Error en delete_transaction: {e}")
        return Response(
            {'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ── BUDGETS ──────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([AllowAny])
def get_budgets(request):
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response(
                {'message': 'Token no proporcionado'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        token = auth_header.split(' ')[1]
        access_token = AccessToken(token)
        user_id = access_token['id']
        
        user = User.objects.get(id=user_id)
        budgets = Budget.objects.filter(user=user, is_active=True).select_related('category').order_by('-start_date')
        serializer = BudgetSerializer(budgets, many=True)
        
        return Response(serializer.data)
    except Exception as e:
        print(f"❌ Error en get_budgets: {e}")
        return Response(
            {'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def create_budget(request):
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response(
                {'message': 'Token no proporcionado'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        token = auth_header.split(' ')[1]
        access_token = AccessToken(token)
        user_id = access_token['id']
        user = User.objects.get(id=user_id)
        
        serializer = BudgetSerializer(data=request.data)
        
        if not serializer.is_valid():
            errors = serializer.errors
            first_error = next(iter(errors.values()))[0]
            return Response(
                {'message': str(first_error)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        budget = serializer.save(user=user)
        
        return Response({
            'message': 'Presupuesto creado exitosamente',
            'budget': BudgetSerializer(budget).data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print(f"❌ Error en create_budget: {e}")
        return Response(
            {'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT'])
@permission_classes([AllowAny])
def update_budget(request, budget_id):
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response(
                {'message': 'Token no proporcionado'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        token = auth_header.split(' ')[1]
        access_token = AccessToken(token)
        user_id = access_token['id']
        user = User.objects.get(id=user_id)
        
        try:
            budget = Budget.objects.get(id=budget_id, user=user)
        except Budget.DoesNotExist:
            return Response(
                {'message': 'Presupuesto no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = BudgetSerializer(budget, data=request.data, partial=True)
        
        if not serializer.is_valid():
            errors = serializer.errors
            first_error = next(iter(errors.values()))[0]
            return Response(
                {'message': str(first_error)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()
        
        return Response({'message': 'Presupuesto actualizado exitosamente'})
        
    except Exception as e:
        print(f"❌ Error en update_budget: {e}")
        return Response(
            {'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_budget(request, budget_id):
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response(
                {'message': 'Token no proporcionado'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        token = auth_header.split(' ')[1]
        access_token = AccessToken(token)
        user_id = access_token['id']
        user = User.objects.get(id=user_id)
        
        try:
            budget = Budget.objects.get(id=budget_id, user=user)
        except Budget.DoesNotExist:
            return Response(
                {'message': 'Presupuesto no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        budget.delete()
        
        return Response({'message': 'Presupuesto eliminado exitosamente'})
        
    except Exception as e:
        print(f"❌ Error en delete_budget: {e}")
        return Response(
            {'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ── GOALS ────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([AllowAny])
def get_goals(request):
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response({'message': 'Token no proporcionado'}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(' ')[1]
        access_token = AccessToken(token)
        user_id = access_token['id']
        user = User.objects.get(id=user_id)

        goals = Goal.objects.filter(user=user).select_related('category').order_by('-created_at')
        serializer = GoalSerializer(goals, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(f"❌ Error en get_goals: {e}")
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_goal(request):
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response({'message': 'Token no proporcionado'}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(' ')[1]
        access_token = AccessToken(token)
        user_id = access_token['id']
        user = User.objects.get(id=user_id)

        data = request.data
        category_id = data.get('category_id')
        category = None
        if category_id:
            try:
                category = Category.objects.get(id=category_id, user=user)
            except Category.DoesNotExist:
                return Response({'message': 'Categoría no encontrada'}, status=status.HTTP_400_BAD_REQUEST)

        goal = Goal.objects.create(
            user=user,
            category=category,
            name=data['name'],
            description=data.get('description', ''),
            target_amount=data['target_amount'],
            target_date=data['target_date'],
            priority=data.get('priority', 'medium'),
            status=data.get('status', 'in_progress'),
        )

        return Response({
            'message': 'Meta creada exitosamente',
            'goal': GoalSerializer(goal).data
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(f"❌ Error en create_goal: {e}")
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([AllowAny])
def update_goal(request, goal_id):
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response({'message': 'Token no proporcionado'}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(' ')[1]
        access_token = AccessToken(token)
        user_id = access_token['id']
        user = User.objects.get(id=user_id)

        try:
            goal = Goal.objects.get(id=goal_id, user=user)
        except Goal.DoesNotExist:
            return Response({'message': 'Meta no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        category_id = data.get('category_id')
        if category_id:
            try:
                goal.category = Category.objects.get(id=category_id, user=user)
            except Category.DoesNotExist:
                return Response({'message': 'Categoría no encontrada'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            goal.category = None

        goal.name          = data.get('name', goal.name)
        goal.description   = data.get('description', goal.description)
        goal.target_amount = data.get('target_amount', goal.target_amount)
        goal.target_date   = data.get('target_date', goal.target_date)
        goal.priority      = data.get('priority', goal.priority)
        goal.status        = data.get('status', goal.status)
        goal.save()

        return Response({
            'message': 'Meta actualizada exitosamente',
            'goal': GoalSerializer(goal).data
        })
    except Exception as e:
        print(f"❌ Error en update_goal: {e}")
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_goal(request, goal_id):
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response({'message': 'Token no proporcionado'}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(' ')[1]
        access_token = AccessToken(token)
        user_id = access_token['id']
        user = User.objects.get(id=user_id)

        try:
            goal = Goal.objects.get(id=goal_id, user=user)
        except Goal.DoesNotExist:
            return Response({'message': 'Meta no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        goal.delete()
        return Response({'message': 'Meta eliminada exitosamente'})
    except Exception as e:
        print(f"❌ Error en delete_goal: {e}")
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ── DEBTS ────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([AllowAny])
def get_debts(request):
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response({'message': 'Token no proporcionado'}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(' ')[1]
        access_token = AccessToken(token)
        user_id = access_token['id']
        user = User.objects.get(id=user_id)

        debts = Debt.objects.filter(user=user).select_related('category').order_by('-created_at')
        serializer = DebtSerializer(debts, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(f"❌ Error en get_debts: {e}")
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_debt(request):
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response({'message': 'Token no proporcionado'}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(' ')[1]
        access_token = AccessToken(token)
        user_id = access_token['id']
        user = User.objects.get(id=user_id)

        data = request.data
        category_id = data.get('category_id')
        category = None
        if category_id:
            try:
                category = Category.objects.get(id=category_id, user=user)
            except Category.DoesNotExist:
                return Response({'message': 'Categoría no encontrada'}, status=status.HTTP_400_BAD_REQUEST)

        amount        = float(data['amount'])
        interest_rate = float(data.get('interest_rate', 0))
        months        = int(data.get('months', 0))

        # Cálculo interés compuesto: total = monto * (1 + tasa/100) ^ meses
        if interest_rate > 0 and months > 0:
            total_with_interest = amount * ((1 + interest_rate / 100) ** months)
        else:
            total_with_interest = amount

        # Si el frontend envía el total ya calculado, lo respetamos
        total_with_interest = float(data.get('total_with_interest', total_with_interest))

        debt = Debt.objects.create(
            user=user,
            category=category,
            name=data['name'],
            creditor_name=data.get('creditor_name', ''),
            amount=amount,
            interest_rate=interest_rate,
            months=months,
            total_with_interest=total_with_interest,
            due_date=data['due_date'],
            description=data.get('description', ''),
            status=data.get('status', 'pending'),
        )

        return Response({
            'message': 'Deuda creada exitosamente',
            'debt': DebtSerializer(debt).data
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(f"❌ Error en create_debt: {e}")
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([AllowAny])
def update_debt(request, debt_id):
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response({'message': 'Token no proporcionado'}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(' ')[1]
        access_token = AccessToken(token)
        user_id = access_token['id']
        user = User.objects.get(id=user_id)

        try:
            debt = Debt.objects.get(id=debt_id, user=user)
        except Debt.DoesNotExist:
            return Response({'message': 'Deuda no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        category_id = data.get('category_id')
        if category_id:
            try:
                debt.category = Category.objects.get(id=category_id, user=user)
            except Category.DoesNotExist:
                return Response({'message': 'Categoría no encontrada'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            debt.category = None

        amount        = float(data.get('amount', debt.amount))
        interest_rate = float(data.get('interest_rate', debt.interest_rate))
        months        = int(data.get('months', debt.months))

        if interest_rate > 0 and months > 0:
            total_with_interest = amount * ((1 + interest_rate / 100) ** months)
        else:
            total_with_interest = amount

        total_with_interest = float(data.get('total_with_interest', total_with_interest))

        debt.name                = data.get('name', debt.name)
        debt.creditor_name       = data.get('creditor_name', debt.creditor_name)
        debt.amount              = amount
        debt.interest_rate       = interest_rate
        debt.months              = months
        debt.total_with_interest = total_with_interest
        debt.due_date            = data.get('due_date', debt.due_date)
        debt.description         = data.get('description', debt.description)
        debt.status              = data.get('status', debt.status)
        debt.save()

        return Response({
            'message': 'Deuda actualizada exitosamente',
            'debt': DebtSerializer(debt).data
        })
    except Exception as e:
        print(f"❌ Error en update_debt: {e}")
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_debt(request, debt_id):
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response({'message': 'Token no proporcionado'}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(' ')[1]
        access_token = AccessToken(token)
        user_id = access_token['id']
        user = User.objects.get(id=user_id)

        try:
            debt = Debt.objects.get(id=debt_id, user=user)
        except Debt.DoesNotExist:
            return Response({'message': 'Deuda no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        debt.delete()
        return Response({'message': 'Deuda eliminada exitosamente'})
    except Exception as e:
        print(f"❌ Error en delete_debt: {e}")
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)