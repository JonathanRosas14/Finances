# Arquitectura

Finances Pro está dividido en un frontend Vue y un backend Django REST.

## Flujo General

```text
Navegador
  ↓
Frontend Vue 3 (Vite)
  ↓ Axios + JWT Bearer token
API Django REST
  ↓
Base de datos PostgreSQL
```

## Responsabilidades Del Frontend

- Enrutar páginas públicas y páginas autenticadas.
- Guardar token JWT y datos del usuario en `localStorage`.
- Consultar y modificar recursos financieros mediante la API.
- Calcular indicadores del dashboard desde los datos recibidos.
- Exportar reportes a PDF y Excel.
- Guardar preferencias visuales localmente.

## Responsabilidades Del Backend

- Autenticar usuarios.
- Validar datos entrantes con serializers.
- Asociar la información financiera al usuario autenticado.
- Persistir usuarios, categorías, transacciones, presupuestos, metas y deudas.
- Exponer endpoints REST para operaciones CRUD.

## Propiedad De Datos

Los datos financieros pertenecen al usuario autenticado mediante relaciones:

- `User -> Category`
- `User -> Transaction`
- `User -> Budget`
- `User -> Goal`
- `User -> Debt`

Las categorías pueden asociarse a transacciones, presupuestos, metas y deudas.

## Preferencias

Las preferencias de tema, región, moneda y periodo default del dashboard son frontend-only y se guardan en `localStorage`.

## Arquitectura De Estilos

La UI tiene dos capas:

- Estilos scoped para necesidades puntuales de cada componente.
- Sistema visual global en `Frontend/src/styles/theme.css` para colores, tarjetas, botones, inputs, tablas y modo oscuro.

## Integraciones Actuales

- API base: `http://localhost:8000/api`.
- Frontend local: `http://localhost:5173`.
- Redirect Google OAuth: `http://localhost:5173/auth-success`.
