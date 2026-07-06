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
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except Exception:
    import traceback
    _error = traceback.format_exc()
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [_error.encode()]
