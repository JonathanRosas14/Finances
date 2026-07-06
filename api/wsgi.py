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
    lines.append('=== /var/task/.vercel_python_packages/ contents ===')
    pkg = Path('/var/task/.vercel_python_packages')
    if pkg.exists():
        for d in sorted(pkg.iterdir()):
            lines.append(f'  {d.name}')
            if d.is_dir() and not d.name.endswith('.dist-info') and not d.name.endswith('.libs'):
                for f in sorted(d.iterdir()):
                    lines.append(f'    {f.name}')
    lines.append('')
    lines.append('=== /var/task/_vendor/psycopg_binary/ contents ===')
    p = Path('/var/task/_vendor/psycopg_binary')
    if p.exists():
        for f in sorted(p.iterdir()):
            lines.append(f'  {f.name}')
    lines.append('')
    lines.append('=== /var/task/_vendor/ contents ===')
    v = Path('/var/task/_vendor')
    for d in sorted(v.iterdir()):
        if d.is_dir() and not d.name.endswith('.dist-info') and not d.name.endswith('.libs'):
            lines.append(f'  {d.name}/')
    lines.append('')
    lines.append('=== try import psycopg ===')
    import importlib
    try:
        # Check if psycopg exists as a module in any path
        spec = importlib.util.find_spec('psycopg')
        lines.append(f'  psycopg spec: {spec}')
    except ImportError as e:
        lines.append(f'  psycopg find_spec failed: {e}')
    lines.append('')
    lines.append('=== try import psycopg_binary ===')
    try:
        import psycopg_binary
        lines.append(f'  psycopg_binary OK: {psycopg_binary.__file__}')
    except ImportError as e:
        lines.append(f'  psycopg_binary FAIL: {e}')
    lines.append('')
    lines.append('=== sys.path ===')
    for i, p in enumerate(sys.path):
        lines.append(f'  {i}: {p}')
    
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
