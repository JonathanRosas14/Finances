import os
import sys
from pathlib import Path

# Check if Backend dir exists
backend_dir = str(Path(__file__).resolve().parent.parent / 'Backend')
sys.path.insert(0, backend_dir)

def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    body = []
    body.append(f'Python: {sys.version}'.encode())
    body.append(f'\nPath: {backend_dir}'.encode())
    body.append(f'\nFiles: {os.listdir(backend_dir) if os.path.exists(backend_dir) else "NOT FOUND"}'.encode())
    return body
