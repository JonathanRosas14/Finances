# Flujo De Desarrollo

## Antes De Trabajar

Revisar cambios actuales:

```bash
git status --short
```

Instalar dependencias si hace falta:

```bash
cd Backend
pip install -r requirements.txt

cd ../Frontend
npm install
```

## Ejecución Local

Usar dos terminales.

Backend:

```bash
cd Backend
source venv/bin/activate
python manage.py runserver 8000
```

Frontend:

```bash
cd Frontend
npm run dev
```

## Verificación

Ejecutar build después de cambios de UI o lógica frontend:

```bash
cd Frontend
npm run build
```

Ejecutar migraciones después de cambios en modelos:

```bash
cd Backend
python manage.py makemigrations
python manage.py migrate
```

## Estilo De Código

- Mantener los componentes Vue enfocados en su responsabilidad.
- Preferir cambios pequeños y directos.
- Mantener la UI alineada con `docs/DESIGN_SYSTEM.md`.
- Reutilizar los patrones de API y manejo de token existentes.
- No versionar `.env`, entornos virtuales ni builds generados.

## Cuándo Actualizar Documentación

Actualizar la documentación cuando cambien:

- Endpoints o payloads de API.
- Variables de entorno.
- Pasos de instalación.
- Convenciones del sistema visual.
- Comportamientos importantes de páginas.
