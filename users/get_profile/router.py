from fastapi import APIRouter, Depends, status, Request
from core.security import oAuth2_scheme
from users.get_profile.responses import UserResponse

router: APIRouter = APIRouter(
    dependencies=[Depends(oAuth2_scheme)],
    prefix='/profile',
    tags=['Profile'],
    responses={404: {'description': 'Nie znaleziono'}}
)


@router.post('/get', status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user_profile(request: Request):
    return request.user
