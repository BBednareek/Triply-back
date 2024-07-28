from pydantic import BaseModel, EmailStr, field_validator
import re


class CreateUserRequest(BaseModel):
    nickname: str
    gender: int
    email: EmailStr
    password: str
    phoneCode: str
    phoneNumber: str

    @classmethod
    @field_validator('phoneCode')
    def validate_phone_code(cls, value: str) -> str:
        if not re.match(r'^\+\d{1,4}$', value):
            raise ValueError("Zły kod kierunkowy!")
        return value

    @classmethod
    @field_validator('phoneNumber')
    def validate_phone_number(cls, value: str) -> str:
        if not value.isdigit() and len(value) > 15:
            raise ValueError("Podano zły numer kontaktowy")
        return value

    @classmethod
    @field_validator('gender')
    def validate_gender(cls, value: str) -> int:
        if value not in (1, 2):
            raise ValueError("Wybierz płeć!")
        return value

    @classmethod
    @field_validator('gender')
    def validate_password(cls, value: str) -> str:
        if (
                len(value) < 8
                or not re.search(r'[A-Z]', value)
                or not re.search(r'[a-z]', value)
                or not re.search(r'[0-9]', value)
                or not re.search(r'[\W_]', value)):
            raise ValueError(
                "Hasło powinno zawierać minimum 8 liter, 1 dużą literę,"
                " 1 małą literę, cyfrę oraz znak specjalny"
            )

        return value
