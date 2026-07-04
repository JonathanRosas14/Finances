# Finances Pro

Finances Pro es una aplicación full-stack para gestionar finanzas personales. Permite registrar ingresos y gastos, organizar categorías, controlar presupuestos, seguir metas, administrar deudas y consultar reportes desde un dashboard central.

## Funcionalidades

- Autenticación local y soporte para Google OAuth.
- Dashboard financiero con indicadores, gráficos y movimientos recientes.
- Gestión de transacciones por categoría y tipo.
- Presupuestos con progreso y umbrales de alerta.
- Metas financieras con cálculo de avance.
- Deudas con interés, vencimiento y progreso de pago.
- Reportes con filtros y exportación a PDF/Excel.
- Configuración de tema, idioma/región, moneda y periodo default del dashboard.

## Stack Tecnológico

- Frontend: Vue 3, Vite, Vue Router, Pinia y Axios.
- Backend: Django, Django REST Framework, Simple JWT y PostgreSQL.
- Exportaciones: jsPDF y xlsx.
- Estilos: CSS scoped por componente y sistema visual global en `Frontend/src/styles/theme.css`.

## Estructura Del Proyecto

```text
Finances_pro/
├── Backend/                 # API Django
│   ├── core/                # Settings y URLs principales
│   ├── finances/            # Modelos, serializers, auth, views y rutas
│   ├── manage.py
│   └── requirements.txt
├── Frontend/                # Cliente Vue/Vite
│   ├── src/components/      # Páginas y componentes
│   ├── src/lib/             # Utilidades compartidas
│   ├── src/router/          # Configuración de rutas
│   └── src/styles/          # Tema global y sistema visual
├── docs/                    # Documentación organizada
├── docker-compose.yml
└── README.md
```

## Inicio Rápido

1. Instalar dependencias del backend:

```bash
cd Backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Configurar variables de entorno:

```bash
cp ../docs/env.example .env
```

3. Ejecutar migraciones y levantar el backend:

```bash
python manage.py migrate
python manage.py runserver 8000
```

4. Instalar dependencias del frontend y levantar Vite:

```bash
cd ../Frontend
npm install
npm run dev
```

5. Abrir la aplicación:

```text
http://localhost:5173
```

## Documentación

- [Instalación y configuración](docs/SETUP.md)
- [Frontend](docs/FRONTEND.md)
- [Backend](docs/BACKEND.md)
- [API](docs/API.md)
- [Arquitectura](docs/ARCHITECTURE.md)
- [Sistema de diseño](docs/DESIGN_SYSTEM.md)
- [Flujo de desarrollo](docs/DEVELOPMENT.md)
- [Notas históricas](docs/LEGACY_NOTES.txt)

## Comandos Principales

Frontend:

```bash
cd Frontend
npm run dev
npm run build
npm run lint
npm run format
```

Backend:

```bash
cd Backend
python manage.py migrate
python manage.py runserver 8000
```

## Notas

- La URL base de la API usada por el frontend es `http://localhost:8000/api`.
- El frontend local corre en `http://localhost:5173`.
- Las peticiones autenticadas usan `Authorization: Bearer <token>`.
- Las preferencias visuales se guardan en `localStorage` bajo la clave `fp_settings`.
