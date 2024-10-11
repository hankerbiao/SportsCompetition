from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import PyJWTError
import jwt

from app.schemas.login import JWTPayload
from app.settings.config import settings


def create_access_token(*, data: JWTPayload):
    payload = data.model_dump().copy()
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


# 假设你的token endpoint是 "/api/token"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/base/access_token")

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        jwt_payload = JWTPayload(**payload)
        user_id: int = jwt_payload.user_id
        if user_id is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    return user_id