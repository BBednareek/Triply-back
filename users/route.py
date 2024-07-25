from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from users.schemas import CreateUserRequest
from users.services import create_user_account
from fastapi.responses import JSONResponse

router: APIRouter = APIRouter(
    prefix='/register',
    tags=['Register'],
    responses={404: {'description': 'Not found'}}
)


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserRequest, db: Session = Depends(get_db)) -> JSONResponse:
    await create_user_account(data=data, db=db)

    payload: dict[str, str] = {"message": "Pomyślnie utworzono konto."}
    return JSONResponse(content=payload, status_code=status.HTTP_201_CREATED)