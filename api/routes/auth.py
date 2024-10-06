import os

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ..models import Token, User, UsersList
from ..services.auth import AuthService, get_current_user

router = APIRouter(
    prefix='',
    tags=["auth"]
)

SECRET = os.environ["JWT_SECRET"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["JWT_EXPIRATION"])

@router.post("/token", response_model=Token)
async def login(request: Request,
                form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                service: AuthService = Depends()):
    user_data = await service.get_user(form_data.username)
    if user_data:
        user = User.from_orm(user_data)
        if service.verify_password(form_data.password, user.password):
            access_token = service.create_access_token(
                data={"sub": user.email},
                expires_delta=timedelta(ACCESS_TOKEN_EXPIRE_MINUTES))
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=400,
                                detail="Incorrect username or password")
    else:
        raise HTTPException(status_code=400,
                            detail="Incorrect username or password")

@router.get("/users")
async def users_list(current_user: Annotated[User, Depends(get_current_user)],
                     service: AuthService = Depends()):
    """
    Test endpoint - allows to get users list

    :param current_user: incoming user data (token)
    :type current_user: Annotated[User, Depends(get_current_user)]
    :param service: used service
    :type service: AuthService

    :rtype: UsersList
    """

    result = await service.users_list()
    return UsersList(data=result)