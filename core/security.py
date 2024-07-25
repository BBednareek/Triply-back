from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
from jose import jwt, JWTError
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from fastapi.param_functions import Header, Depends
from sqlalchemy.orm import Session
from core.config import get_settings, Settings
from core.database import get_db
from typing import Optional
from users.register.models.user_model import UserModel

settings: Settings = get_settings()
pwd_context: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')
oAuth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/register/token")


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


def get_current_user(token: str = Depends(oAuth2_scheme), db=None) -> Optional[UserModel]:
    payload: dict[str, any] = get_token_payload(token)

    if not payload or type(payload) is not dict:
        return None

    user_id: Optional[int] = payload.get('id', None)

    if not user_id:
        return None

    if not db:
        db = next(get_db())

    user: Optional[UserModel] = db.query(UserModel).filter(user_id == UserModel.id).first()

    return user


class JWTAuth:

    @staticmethod
    async def authenticate(conn: Header) -> (tuple[AuthCredentials, UnauthenticatedUser]
                                             | tuple[AuthCredentials, UserModel]):

        guest: tuple[AuthCredentials, UnauthenticatedUser] = (AuthCredentials(['unauthenticated']),
                                                              UnauthenticatedUser())

        if 'authorization' not in conn.headers:
            return guest

        token: str = conn.headers['authorization'].split(' ')[1]

        if not token:
            return guest

        user: UserModel = get_current_user(token)

        if not user:
            return guest

        return AuthCredentials('authenticated'), user
