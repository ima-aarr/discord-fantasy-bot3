import os, requests
BASE = os.getenv('FIREBASE_URL')
SECRET = os.getenv('FIREBASE_SECRET')
if not BASE:
    raise RuntimeError('FIREBASE_URL not set')
if not BASE.endswith('/'):
    BASE = BASE + '/'
def _url(path: str):
    path = path.strip('/')
    url = f"{BASE}{path}.json"
    if SECRET:
        sep = '&' if '?' in url else '?'
        url = f"{url}{sep}auth={SECRET}"
    return url
def get(path: str):
    r = requests.get(_url(path), timeout=20)
    if r.status_code == 200: return r.json()
    if r.status_code == 404: return None
    r.raise_for_status()
def put(path: str, data):
    r = requests.put(_url(path), json=data, timeout=20); r.raise_for_status(); return r.json()
def post(path: str, data):
    r = requests.post(_url(path), json=data, timeout=20); r.raise_for_status(); return r.json()
def delete(path: str):
    r = requests.delete(_url(path), timeout=20); r.raise_for_status(); return r.json()
