# API

URL base:

```text
http://localhost:8000/api
```

La mayoría de endpoints requieren:

```text
Authorization: Bearer <token>
```

Los endpoints de autenticación no requieren token previo.

## Autenticación

| Método | Endpoint | Descripción |
| --- | --- | --- |
| POST | `/register/` | Crear cuenta local. |
| POST | `/login/` | Iniciar sesión con email/password y recibir tokens. |
| POST | `/google/` | Autenticación con Google. |

Payload de registro:

```json
{
  "username": "jane",
  "email": "jane@example.com",
  "password": "Password1"
}
```

Payload de login:

```json
{
  "email": "jane@example.com",
  "password": "Password1"
}
```

## Categorías

| Método | Endpoint | Descripción |
| --- | --- | --- |
| GET | `/categories/` | Lista categorías del usuario. |
| POST | `/categories/create/` | Crea una categoría. |
| PUT | `/categories/<category_id>/` | Actualiza una categoría. |
| DELETE | `/categories/<category_id>/delete/` | Elimina una categoría. |

Payload:

```json
{
  "name": "Food",
  "icon": "box",
  "color": "#1a7f3a",
  "type": "expense",
  "parent_id": null
}
```

## Transacciones

| Método | Endpoint | Descripción |
| --- | --- | --- |
| GET | `/transactions/` | Lista transacciones. |
| POST | `/transactions/create/` | Crea una transacción. |
| PUT | `/transactions/<transaction_id>/` | Actualiza una transacción. |
| DELETE | `/transactions/<transaction_id>/delete/` | Elimina una transacción. |

Payload:

```json
{
  "amount": "45.90",
  "transaction_date": "2026-05-07",
  "description": "Groceries",
  "category_id": 1,
  "type": "expense",
  "payment_method": "cash",
  "is_recurring": false,
  "recurring_frequency": null,
  "notes": "Weekly supermarket"
}
```

## Presupuestos

| Método | Endpoint | Descripción |
| --- | --- | --- |
| GET | `/budgets/` | Lista presupuestos. |
| POST | `/budgets/create/` | Crea un presupuesto. |
| PUT | `/budgets/<budget_id>/` | Actualiza un presupuesto. |
| DELETE | `/budgets/<budget_id>/delete/` | Elimina un presupuesto. |

Payload:

```json
{
  "name": "Food Budget",
  "category": 1,
  "amount": "500.00",
  "period": "monthly",
  "start_date": "2026-05-01",
  "end_date": "2026-05-31",
  "alert_percentage": 80,
  "is_active": true,
  "description": "Monthly food spending limit"
}
```

## Metas

| Método | Endpoint | Descripción |
| --- | --- | --- |
| GET | `/goals/` | Lista metas. |
| POST | `/goals/create/` | Crea una meta. |
| PUT | `/goals/<goal_id>/` | Actualiza una meta. |
| DELETE | `/goals/<goal_id>/delete/` | Elimina una meta. |

Payload:

```json
{
  "name": "Emergency Fund",
  "description": "Three months of expenses",
  "target_amount": "3000.00",
  "target_date": "2026-12-31",
  "category_id": 2,
  "priority": "high",
  "status": "in_progress"
}
```

## Deudas

| Método | Endpoint | Descripción |
| --- | --- | --- |
| GET | `/debts/` | Lista deudas. |
| POST | `/debts/create/` | Crea una deuda. |
| PUT | `/debts/<debt_id>/` | Actualiza una deuda. |
| DELETE | `/debts/<debt_id>/delete/` | Elimina una deuda. |

Payload:

```json
{
  "name": "Credit Card",
  "creditor_name": "Bank",
  "amount": "1200.00",
  "interest_rate": "2.50",
  "months": 6,
  "total_with_interest": "1391.63",
  "due_date": "2026-11-30",
  "category_id": 3,
  "description": "Card balance",
  "status": "in_progress"
}
```

## Campos Comunes De Respuesta

Las respuestas de listado suelen devolver arrays de objetos con:

- `id`
- campos propios del recurso
- `created_at`
- helpers de visualización como `category_name` cuando aplica

## Validaciones Importantes

- Los montos deben ser mayores a cero.
- La fecha de transacción es obligatoria.
- La contraseña de registro debe tener mínimo 8 caracteres, una mayúscula y un número.
- Los nombres de categoría son únicos por usuario y tipo.
