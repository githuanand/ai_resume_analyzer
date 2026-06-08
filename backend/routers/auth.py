from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

from database.schemas import (
    UserRegister,
    UserLogin
)

from services.user_service import UserService

from dependencies.services import (
    get_user_service
)

router = APIRouter()


@router.post("/register")
def register(
    user: UserRegister,

    user_service: UserService = Depends(
        get_user_service
    )
):

    try:

        user_service.register(
            email=user.email,
            password=user.password
        )

        return {
            "message": "User registered successfully"
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/login")
def login(
    user: UserLogin,

    user_service: UserService = Depends(
        get_user_service
    )
):

    try:

        token = user_service.login(
            email=user.email,
            password=user.password
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except Exception as e:

        raise HTTPException(
            status_code=401,
            detail=str(e)
        )