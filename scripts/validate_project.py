from __future__ import annotations
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    'README.md', '.env.example', 'docker-compose.yml', 'Makefile',
    'frontend/package.json', 'frontend/src/app/page.tsx', 'frontend/src/app/dashboard/page.tsx',
    'docs/architecture.md', 'docs/api.md', 'docs/database.md', 'docs/events.md', 'docs/testing.md', 'docs/deployment.md',
]
services = ['user-service','product-service','cart-service','order-service','payment-service','notification-service','api-gateway']
for svc in services:
    required.extend([f'services/{svc}/Dockerfile', f'services/{svc}/requirements.txt', f'services/{svc}/app/main.py'])
missing = [p for p in required if not (ROOT / p).exists()]
empty = [str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p.stat().st_size == 0]
if missing or empty:
    print('AstraCart validation failed')
    if missing: print('Missing:', *missing, sep='\n - ')
    if empty: print('Empty files:', *empty, sep='\n - ')
    sys.exit(1)
print(f'AstraCart validation passed: {len(list(ROOT.rglob("*")))} paths checked, no required files missing, no empty files.')
