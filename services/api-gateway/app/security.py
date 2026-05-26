import jwt
from app.config import get_settings

def decode_optional(authorization: str | None) -> dict:
    if not authorization or not authorization.lower().startswith('bearer '): return {'sub':'anonymous','role':'ANONYMOUS','authenticated':False}
    token=authorization.split(' ',1)[1]
    try:
        p=jwt.decode(token, get_settings().jwt_secret_key, algorithms=[get_settings().jwt_algorithm], options={'verify_iss': False})
        return {'sub': p.get('sub','anonymous'), 'role': p.get('role','CUSTOMER'), 'authenticated': True}
    except jwt.PyJWTError:
        return {'sub':'anonymous','role':'ANONYMOUS','authenticated':False, 'invalid': True}

def limit_for(role: str) -> int:
    if role == 'ADMIN': return 300
    if role in {'CUSTOMER','SELLER','SUPPORT'}: return 100
    return 30
