from sqlalchemy.orm import Session
from .user_model import UserBD
from .user_schema import UserCreate, UserUpdate
from .user_schema import User


def get_user(db: Session, user_id: int) -> User:
    return db.query(UserBD).filter(UserBD.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(UserBD).filter(UserBD.email == email).first()


def get_user_email_exclude_id(db: Session, user_id: int, email: str) -> list[User]:
    return db.query(UserBD).filter(UserBD.id != user_id).filter(UserBD.email == email).all()


def get_users(db: Session, skip: int = 0, limit: int = 50) -> list[User]:
    return db.query(UserBD).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    user_db = UserBD(name=user.name, email=user.email, password=user.password)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


def update_user(db: Session, user_id: int, user: UserUpdate):
    db.query(UserBD).filter(UserBD.id == user_id).update(user)
    db.commit()


def del_user(db: Session, email: str):
    user_db = db.query(UserBD).filter(UserBD.email == email).first()
    db.delete(user_db)
    db.commit()
