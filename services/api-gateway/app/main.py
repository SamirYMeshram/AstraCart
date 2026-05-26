from __future__ import annotations
import time
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
import httpx
from app.config import get_settings
from app.rate_limit import check_rate_limit
from app.responses import fail, ok
from app.security import decode_optional
settings=get_settings(); app=FastAPI(title='AstraCart API Gateway', version='2.0.0')
app.add_middleware(CORSMiddleware, allow_origins=[o.strip() for o in settings.cors_origins.split(',')], allow_methods=['*'], allow_headers=['*'])
SERVICE_ROUTES={
    'auth': settings.user_service_url, 'users': settings.user_service_url, 'admin/users': settings.user_service_url,
    'products': settings.product_service_url, 'categories': settings.product_service_url, 'inventory': settings.product_service_url,
    'cart': settings.cart_service_url, 'orders': settings.order_service_url, 'admin/orders': settings.order_service_url,
    'payments': settings.payment_service_url, 'notifications': settings.notification_service_url,
}
def target_for(path: str) -> str | None:
    clean=path.strip('/')
    for prefix, url in sorted(SERVICE_ROUTES.items(), key=lambda x: len(x[0]), reverse=True):
        if clean == prefix or clean.startswith(prefix + '/'):
            return url
    return None
@app.middleware('http')
async def request_context(request: Request, call_next):
    start=time.perf_counter(); response=await call_next(request); response.headers['X-Gateway']='AstraCart'; response.headers['X-Process-Time-Ms']=str(round((time.perf_counter()-start)*1000,2)); return response
@app.exception_handler(HTTPException)
async def http_error(_, exc: HTTPException): return JSONResponse(status_code=exc.status_code, content=fail('Request failed', str(exc.detail)))
@app.exception_handler(Exception)
async def unhandled(_, exc: Exception): return JSONResponse(status_code=500, content=fail('Gateway internal error', str(exc)))
@app.get('/health')
async def health():
    results={}
    async with httpx.AsyncClient(timeout=3) as client:
        for name, url in [('user',settings.user_service_url),('product',settings.product_service_url),('cart',settings.cart_service_url),('order',settings.order_service_url),('payment',settings.payment_service_url),('notification',settings.notification_service_url)]:
            try:
                r=await client.get(f'{url}/health'); results[name]={'healthy': r.status_code==200, 'status_code': r.status_code}
            except Exception as exc:
                results[name]={'healthy': False, 'error': str(exc)}
    return ok('Gateway healthy', {'service': settings.service_name, 'dependencies': results})
@app.api_route('/{full_path:path}', methods=['GET','POST','PATCH','PUT','DELETE'])
async def proxy(full_path: str, request: Request, authorization: str | None = Header(default=None)):
    actor=decode_optional(authorization)
    if actor.get('invalid'): raise HTTPException(status_code=401, detail='Invalid token')
    check_rate_limit(request, actor)
    base=target_for(full_path)
    if not base: raise HTTPException(status_code=404, detail='No service route registered for path')
    body=await request.body()
    headers={k:v for k,v in request.headers.items() if k.lower() not in {'host','content-length'}}
    headers['X-User-Id']=actor.get('sub','anonymous'); headers['X-User-Role']=actor.get('role','ANONYMOUS')
    url=f'{base}/{full_path}'
    async with httpx.AsyncClient(timeout=20) as client:
        upstream=await client.request(request.method, url, params=request.query_params, content=body, headers=headers)
    return Response(content=upstream.content, status_code=upstream.status_code, headers={'Content-Type': upstream.headers.get('content-type','application/json'), 'X-Upstream-Service': base})
