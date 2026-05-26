from __future__ import annotations
import time
from collections import defaultdict
import redis
from fastapi import HTTPException, Request
from app.config import get_settings
from app.security import limit_for

_memory: dict[str, list[float]] = defaultdict(list)
try:
    _redis = redis.Redis.from_url(get_settings().redis_url, decode_responses=True)
    _redis.ping()
except Exception:
    _redis = None

def check_rate_limit(request: Request, actor: dict) -> None:
    role = actor.get('role','ANONYMOUS')
    limit = limit_for(role)
    ident = actor.get('sub') if actor.get('authenticated') else request.client.host if request.client else 'unknown'
    key = f'rl:{role}:{ident}:{int(time.time()//60)}'
    if _redis:
        count = _redis.incr(key)
        if count == 1: _redis.expire(key, 70)
        if count > limit: raise HTTPException(status_code=429, detail=f'Rate limit exceeded: {limit}/minute')
    else:
        now=time.time(); bucket=_memory[key]; bucket[:] = [t for t in bucket if now-t < 60]; bucket.append(now)
        if len(bucket) > limit: raise HTTPException(status_code=429, detail=f'Rate limit exceeded: {limit}/minute')
