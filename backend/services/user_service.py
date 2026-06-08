from repositories.user_repository import UserRepository

from services.auth_service import (
    hash_password,
    verify_password,
    create_access_token
)


class UserService:

    def __init__(
        self,
        user_repo: UserRepository
    ):
        self.user_repo = user_repo

    def register(
        self,
        email: str,
        password: str
    ):

        existing_user = (
            self.user_repo.get_by_email(
                email
            )
        )

        if existing_user:
            raise Exception(
                "Email already exists"
            )

        return self.user_repo.create(
            email=email,
            password=hash_password(
                password
            )
        )

    def login(
        self,
        email: str,
        password: str
    ):

        user = (
            self.user_repo.get_by_email(
                email
            )
        )

        if not user:
            raise Exception(
                "Invalid credentials"
            )

        if not verify_password(
            password,
            user.password
        ):
            raise Exception(
                "Invalid credentials"
            )

        token = create_access_token(
            {
                "sub": user.email
            }
        )

        return token

    def get_by_email(
        self,
        email: str
    ):

        return self.user_repo.get_by_email(
            email
        )