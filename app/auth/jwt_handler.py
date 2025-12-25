from datetime import datetime, timedelta
from jose import jwt

SECRET = "YOURLONGSECRET"           # later load from .env
ALGORITHM = "HS256"
EXPIRES = 60 * 24                   # 1 day

def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=EXPIRES)
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)
