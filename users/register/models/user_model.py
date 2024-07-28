from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from core.database import Base


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    verified = Column(Boolean, default=False, nullable=False)
    nickname = Column(String(15), nullable=False)
    gender = Column(Integer, nullable=False)
    phoneCode = Column(String(5), nullable=False)
    phoneNumber = Column(String(15), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
