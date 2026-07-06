import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'Backend'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

def application(environ, start_response):
    status = '500 Error'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    return [b'Django failed']

try:
    import traceback

    lines = []
    lines.append(f'CWD: {os.getcwd()}')
    lines.append(f'__file__: {__file__}')
    lines.append('')
    lines.append('=== /var/task contents ===')
    for p in Path('/var/task').iterdir():
        lines.append(f'  {p}')
    lines.append('')
    lines.append('=== /var/task/.vercel/ contents ===')
    vercel_path = Path('/var/task/.vercel')
    if vercel_path.exists():
        for p in vercel_path.rglob('*'):
            lines.append(f'  {p}')
    else:
        lines.append('  (does not exist)')
    lines.append('')
    lines.append('=== sys.path ===')
    for i, p in enumerate(sys.path):
        lines.append(f'  {i}: {p}')
    lines.append('')
    lines.append('=== trying site.addsitedir ===')
    try:
        import site
        lines.append(f'  site-packages: {site.getsitepackages()}')
        for sp in site.getsitepackages():
            if sp not in sys.path:
                lines.append(f'  adding {sp}')
                sys.path.insert(0, sp)
    except Exception as e:
        lines.append(f'  site error: {e}')
    lines.append('')
    lines.append('=== try import psycopg again ===')
    try:
        import psycopg
        lines.append(f'  psycopg OK: {psycopg.__file__}')
    except ImportError as e:
        lines.append(f'  psycopg FAIL: {e}')
        lines.append('')
        lines.append('=== searching for psycopg files ===')
        for root in ['/var/task', '/var/lang']:
            for fp in Path(root).rglob('psycopg*'):
                lines.append(f'  found: {fp}')

    body = '\n'.join(lines)

    def application(environ, start_response):
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [body.encode()]
except Exception:
    _error = traceback.format_exc()
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [_error.encode()]
