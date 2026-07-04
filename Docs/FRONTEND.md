# Frontend

El frontend es una aplicación Vue 3 construida con Vite.

## Ubicación

```text
Frontend/
```

## Dependencias Principales

- `vue`: framework UI.
- `vue-router`: rutas.
- `pinia`: manejo de estado disponible para la app.
- `axios`: cliente HTTP.
- `jspdf`: exportación de PDF en reportes.
- `xlsx`: exportación de Excel en reportes.

## Comandos

```bash
npm run dev       # Servidor local
npm run build     # Build de producción
npm run preview   # Preview del build
npm run lint      # Lint configurado
npm run format    # Formatea src/ con Prettier
```

## Rutas

Las rutas están en:

```text
Frontend/src/router/index.js
```

Rutas públicas:

- `/`
- `/features`
- `/about`
- `/contact`
- `/login`
- `/register`
- `/auth-success`

Rutas del workspace autenticado:

- `/Dashboard`
- `/budgets`
- `/goals`
- `/debts`
- `/categories`
- `/transactions`
- `/reports`
- `/settings`

## Componentes Principales

- `MainPage.vue`: layout autenticado y sidebar.
- `Dashboard.vue`: resumen financiero y gráficos.
- `Transactions.vue`: CRUD de transacciones.
- `Categories.vue`: CRUD de categorías.
- `Budgets.vue`: CRUD de presupuestos y progreso.
- `Goals.vue`: CRUD de metas y progreso.
- `Debts.vue`: CRUD de deudas y progreso.
- `Reports.vue`: reportes filtrados y exportaciones.
- `Settings.vue`: preferencias locales y mantenimiento de sesión.
- `ConfirmDialogHost.vue`: modal global de confirmación.

## Patrón De API

Los componentes usan Axios con el token JWT guardado en `localStorage`:

```js
const token = localStorage.getItem('token')

axios.get('http://localhost:8000/api/transactions', {
  headers: { Authorization: `Bearer ${token}` },
})
```

## Preferencias Locales

Las preferencias de UI se guardan en:

```text
localStorage.fp_settings
```

Utilidades relacionadas:

```text
Frontend/src/lib/appSettings.js
```

Preferencias disponibles:

- `theme`
- `locale`
- `currencyCode`
- `dashboardDefaultPeriod`

## Estilos

Los componentes pueden mantener CSS scoped. Las reglas compartidas están en:

```text
Frontend/src/styles/theme.css
```

Para páginas nuevas, reutilizar las clases y patrones definidos en el sistema de diseño.
