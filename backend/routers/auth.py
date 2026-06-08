from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

from sqlalchemy.orm import Session

from database.db import get_db

from database.schemas import (
    UserRegister,
    UserLogin
)

from repositories.user_repository import UserRepository

from services.auth_service import AuthService


router = APIRouter()


@router.post("/register")
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    user_repo = UserRepository(db)

    auth_service = AuthService(
        user_repo=user_repo
    )

    try:

        auth_service.register(
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
    db: Session = Depends(get_db)
):

    user_repo = UserRepository(db)

    auth_service = AuthService(
        user_repo=user_repo
    )

    try:

        token = auth_service.login(
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