from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from users.models.user_model import UserModel
from typing import Optional
from core.security import verify_password, create_access_token, create_refresh_token, get_token_payload
from core.config import Settings, get_settings
from datetime import timedelta
from auth.response import TokenResponse

settings: Settings = get_settings()


async def get_token(data: OAuth2PasswordRequestForm, db: Session) -> TokenResponse:
    user: Optional[UserModel] = db.query(UserModel).filter(data.username == UserModel.email).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Adres mailowy nie występuje w naszej bazie",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Podano błędne hasło",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return await _get_user_token(user=user)


async def get_refresh_token(token: str, db: Session) -> TokenResponse:
    payload: dict[any, any] = get_token_payload(token=token)
    user_id: None = payload.get('id', None)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Błędny refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user: Optional[UserModel] = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Błędny refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return await _get_user_token(user=user, refresh_token=token)


async def _get_user_token(user: UserModel, refresh_token=None) -> TokenResponse:
    payload: dict[str, int] = {"id": user.id}

    access_token_expiry: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token: str = await create_access_token(payload, access_token_expiry)
    if not refresh_token:
        refresh_token: str = await create_refresh_token(payload)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_token_expiry.seconds
    )
