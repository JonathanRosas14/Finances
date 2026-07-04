# Instalación Y Configuración

Guía para ejecutar Finances Pro localmente.

## Requisitos

- Node.js `20.19+` o `22.12+`.
- Python `3.11+` recomendado.
- PostgreSQL local o en Docker.
- Git.

## Backend

Desde la raíz del repositorio:

```bash
cd Backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Crear el archivo `.env` en `Backend/` usando el ejemplo:

```bash
cp ../docs/env.example .env
```

Ejecutar migraciones:

```bash
python manage.py migrate
```

Levantar la API:

```bash
python manage.py runserver 8000
```

URL del backend:

```text
http://localhost:8000
```

URL base de la API:

```text
http://localhost:8000/api
```

## Frontend

Desde la raíz del repositorio:

```bash
cd Frontend
npm install
npm run dev
```

URL del frontend:

```text
http://localhost:5173
```

## Verificación De Build

Antes de cerrar cambios de frontend:

```bash
cd Frontend
npm run build
```

## Problemas Comunes

Si el frontend no se conecta al backend, revisar:

- El backend está corriendo en el puerto `8000`.
- El frontend está corriendo en el puerto `5173`.
- `CORS_ALLOWED_ORIGINS` permite `http://localhost:5173`.
- El usuario inició sesión y existe un JWT válido.

Si el backend no conecta a PostgreSQL, revisar:

- PostgreSQL está activo.
- Las variables `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` y `DB_PORT` son correctas.
- Las migraciones fueron aplicadas.
