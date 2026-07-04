# Sistema De Diseño

Finances Pro usa una línea visual limpia enfocada en finanzas: acentos verdes, bordes suaves, tarjetas blancas y jerarquía clara.

## Fuente Principal

Los estilos globales viven en:

```text
Frontend/src/styles/theme.css
```

Los componentes pueden tener CSS scoped, pero las páginas nuevas deben reutilizar los patrones existentes.

## Principios

- Usar layouts basados en tarjetas.
- Mantener bordes redondeados consistentes.
- Usar verde para acciones principales y valores positivos.
- Usar rojo solo para acciones destructivas o valores negativos.
- Mantener tablas, filtros y formularios alineados visualmente.
- Soportar modo claro y modo oscuro.

## Tokens CSS

Variables globales principales:

- `--fp-bg`
- `--fp-surface`
- `--fp-surface-soft`
- `--fp-border`
- `--fp-border-strong`
- `--fp-primary`
- `--fp-primary-strong`
- `--fp-primary-soft`
- `--fp-text`
- `--fp-muted`
- `--fp-danger`
- `--fp-warning`
- `--fp-radius-lg`
- `--fp-radius-md`
- `--fp-shadow`
- `--fp-shadow-header`

## Patrón De Página Interna

```text
<page-container>
  <header class="*-header">
    <h1>Título</h1>
  </header>

  <main class="*-content">
    <section/card/panel>
      Contenido
    </section/card/panel>
  </main>
</page-container>
```

## Clases Comunes

- Headers: `dashboard-header`, `budgets-header`, `settings-header`, etc.
- Contenido: `dashboard-content`, `budgets-content`, etc.
- Cards/paneles: `panel`, `summary-card`, `settings-panel`, `budget-card`, `goal-card`, `debt-card`.
- Formularios: `form-input`, `filter-input`, `form-group`, `form-row`.
- Botones: `primary-btn`, `ghost-btn`, `danger-btn`, `btn-create`, `btn-submit`.
- Tablas: `transactions-table`.
- Estados vacíos: `empty-state`.
- Progreso: `progress-bar`, `progress-fill`.

## Modo Oscuro

El modo oscuro se controla con:

```text
html[data-theme='dark']
```

El tema se aplica desde `appSettings.js` y se modifica en `Settings.vue`.
