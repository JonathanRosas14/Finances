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
    try:
        import psycopg
        psycopg_ok = f'psycopg OK: {psycopg.__file__}'
    except ImportError as e:
        psycopg_ok = f'psycopg FAIL: {e}'

    try:
        import psycopg2
        psycopg2_ok = f'psycopg2 OK: {psycopg2.__file__}'
    except ImportError as e:
        psycopg2_ok = f'psycopg2 FAIL: {e}'

    sys_path = '\n'.join(sys.path)

    def application(environ, start_response):
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        body = f'{psycopg_ok}\n{psycopg2_ok}\n\nSys.path:\n{sys_path}'
        return [body.encode()]
except Exception:
    import traceback
    _error = traceback.format_exc()
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [_error.encode()]
