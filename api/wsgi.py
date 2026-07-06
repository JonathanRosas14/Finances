import os, sys
from pathlib import Path

backend = Path(__file__).resolve().parent.parent / 'Backend'
sys.path.insert(0, str(backend))

def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    body = [b'Backend exists: ']
    body.append(str(backend.exists()).encode())
    if backend.exists():
        body.append(b'\nContents: ')
        body.append(str([str(p.name) for p in backend.iterdir()]).encode())
    return body
