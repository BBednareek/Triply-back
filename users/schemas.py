from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    nickname: str
    gender: int
    email: EmailStr
    password: str
    phoneCode: str
    phoneNumber: str
