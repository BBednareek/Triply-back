from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from datetime import datetime
from core.database import Base


class UserModel(Base):
    __tablename__: str = 'users'
    id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String(255), unique=True, nullable=False)
    password: str = Column(String(100), nullable=False)
    verified: bool = Column(Boolean, nullable=False)
    nickname: str = Column(String(15), nullable=False)
    gender: int = Column(Integer, nullable=False)
    phoneCode: str = Column(String(5), nullable=False)
    phoneNumber: str = Column(String(15), nullable=False)
    created_at: datetime = Column(DateTime, server_default=func.now(), nullable=False)
