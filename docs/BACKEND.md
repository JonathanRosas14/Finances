# Backend

El backend es una API REST construida con Django y Django REST Framework.

## Ubicación

```text
Backend/
```

## Dependencias Principales

- `Django`
- `djangorestframework`
- `djangorestframework-simplejwt`
- `django-cors-headers`
- `psycopg2-binary`
- `python-dotenv`
- `social-auth-app-django`
- `google-auth`
- `bcrypt`

## Estructura

```text
Backend/
├── core/
│   ├── settings.py       # Configuración Django
│   └── urls.py           # URLs principales
├── finances/
│   ├── authentication.py # Autenticación JWT custom
│   ├── models.py         # Modelos de datos
│   ├── serializers.py    # Serializers y validaciones
│   ├── urls.py           # Rutas de la API
│   └── views.py          # Handlers de endpoints
├── manage.py
└── requirements.txt
```

## Configuración

Las variables se leen desde `Backend/.env`.

Variables importantes:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `DB_ENGINE`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `JWT_SECRET`
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`

Ver [env.example](env.example).

## Modelos

- `User`: identidad de usuario local o Google.
- `Category`: categorías de ingreso o gasto por usuario.
- `Transaction`: registros de ingresos y gastos.
- `Budget`: límites de gasto por periodo y categoría opcional.
- `Goal`: metas financieras.
- `Debt`: deudas con interés, fecha límite y estado.

## Autenticación

La API usa JWT mediante:

```text
finances.authentication.CustomJWTAuthentication
```

Las peticiones autenticadas deben enviar:

```text
Authorization: Bearer <access_token>
```

## CORS

Orígenes permitidos para desarrollo:

```text
http://localhost:5173
http://127.0.0.1:5173
```

## Comandos Útiles

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 8000
```
