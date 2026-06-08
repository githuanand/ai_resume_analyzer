from sqlalchemy.orm import Session

from database.models import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):

        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def get_by_id(self, user_id: int):

        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def create(self, email: str, password: str):

        user = User(
            email=email,
            password=password
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user