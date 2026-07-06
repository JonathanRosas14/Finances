import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent / 'Backend'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
