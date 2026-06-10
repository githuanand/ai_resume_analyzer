from repositories.user_repository import UserRepository

from passlib.context import CryptContext

from jose import jwt
from datetime import datetime, timedelta


SECRET_KEY = "resume_saas_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
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
            password=self.hash_password(
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

        if not self.verify_password(
            password,
            user.password
        ):
            raise Exception(
                "Invalid credentials"
            )

        return self.create_access_token(
            {
                "sub": user.email
            }
        )

    def hash_password(
        self,
        password: str
    ):
        return pwd_context.hash(
            password
        )

    def verify_password(
        self,
        plain_password: str,
        hashed_password: str
    ):
        return pwd_context.verify(
            plain_password,
            hashed_password
        )

    def create_access_token(
        self,
        data: dict
    ):

        to_encode = data.copy()

        expire = (
            datetime.utcnow()
            + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        )

        to_encode.update(
            {"exp": expire}
        )

        return jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

    def get_by_email(
        self,
        email: str
    ):
        return self.user_repo.get_by_email(
            email
        )