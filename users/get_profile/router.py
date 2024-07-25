from fastapi import APIRouter, Depends, status, Request
from core.security import oAuth2_scheme, get_current_user

router: APIRouter = APIRouter(
    dependencies=[
        Depends(oAuth2_scheme),
        Depends(get_current_user)
    ],
    prefix='/profile',
    tags=['Profile'],
    responses={404: {'description': 'Nie znaleziono'}}
)


@router.post('/get', status_code=status.HTTP_200_OK)
def get_user_profile(request: Request):
    return request.user
