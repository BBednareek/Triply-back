from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
from jose import jwt, JWTError
from core.config import get_settings, Settings

settings: Settings = get_settings()
pwd_context: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')
oAuth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def create_access_token(data: dict[any, any], expiry: timedelta) -> str:
    payload: dict[any, any] = data.copy()

    expire_in: datetime = datetime.now() + expiry

    payload.update({'exp': expire_in})

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )


async def create_refresh_token(data: dict[any, any]) -> str:
    return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def get_token_payload(token: str) -> dict[any, any]:
    try:
        payload: dict[any, any] = jwt.decode(token, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM)
    except JWTError as e:
        raise JWTError(str(e))

    return payload
