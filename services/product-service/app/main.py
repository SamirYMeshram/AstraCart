from __future__ import annotations
import time
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import get_settings
from app.core.database import Base, engine
from app.core.responses import fail
from app.routers import router
settings = get_settings()
app = FastAPI(title='AstraCart Product Service', version='2.0.0')
app.add_middleware(CORSMiddleware, allow_origins=[o.strip() for o in settings.cors_origins.split(',')], allow_methods=['*'], allow_headers=['*'])
@app.middleware('http')
async def timer(request: Request, call_next):
    start=time.perf_counter(); response=await call_next(request); response.headers['X-Service']=settings.service_name; response.headers['X-Process-Time-Ms']=str(round((time.perf_counter()-start)*1000,2)); return response

@app.exception_handler(HTTPException)
async def http_error(_, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content=fail('Request failed', str(exc.detail)))

@app.exception_handler(Exception)
async def unhandled(_, exc: Exception):
    return JSONResponse(status_code=500, content=fail('Internal server error', str(exc)))
@app.on_event('startup')
def startup(): Base.metadata.create_all(bind=engine, checkfirst=True)
@app.get('/health')
def health(): return {'success': True, 'message': 'product-service healthy', 'data': {'service': settings.service_name}}
app.include_router(router)
