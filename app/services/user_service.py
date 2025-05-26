from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate

def create_user(db: Session, user: UserCreate) -> User:
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=user.hashed_password,
        role="user",
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_users(db: Session) -> list[User]:
    return db.query(User).all()
