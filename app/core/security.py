
from datetime import datetime, timedelta,timezone
from jose import JWTError, jwt
from app.core.config import settings

def create_access_token(data: dict, expire_minutes = 30):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.JWT_SCRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

def verify_access_token(token : str):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SCRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload 
    except JWTError:
        return None

