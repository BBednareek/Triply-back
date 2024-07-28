from users.register.models.user_model import UserModel
from fastapi.exceptions import HTTPException
from core.security import get_password_hash
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from users.register.schemas import CreateUserRequest
from fastapi import status
from pydantic import ValidationError
from logging import exception as logging_exception


async def create_user_account(data: CreateUserRequest, db: Session) -> UserModel:
    try:
        user: Optional[UserModel] = db.query(UserModel).filter(data.email == UserModel.email).first()

        if user:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Ten adres email już istnieje w naszej bazie!")

        new_user: UserModel = UserModel(
            email=data.email,
            password=get_password_hash(data.password),
            nickname=data.nickname,
            verified=False,
            gender=data.gender,
            phoneCode=data.phoneCode,
            phoneNumber=data.phoneNumber,
            created_at=datetime.now(),
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors())

    except HTTPException as e:
        raise e

    except Exception as e:
        logging_exception("Nieznany błąd: " + e)
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Serwer nie odpowiada",
        )
