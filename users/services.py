from users.models.user_model import UserModel
from fastapi.exceptions import HTTPException, ValidationException
from core.security import get_password_hash
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from users.schemas import CreateUserRequest
from fastapi import status


async def create_user_account(data: CreateUserRequest, db: Session) -> UserModel:
    try:
        data = CreateUserRequest(**data.model_dump())

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
        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return new_user

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str("Serwer nie odpowiada"))

    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors())
