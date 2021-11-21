from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from .user_schema import User, UserUpdate, UserDelete, UserCreate, UserUpdateAttr
from typing import List
from .user_controller import (
    get_user,
    get_users,
    get_user_by_email,
    create_user,
    del_user,
    update_user,
    get_user_email_exclude_id
 )
from .util import get_password_hash, verify_password


user_route = APIRouter()


@user_route.post("/users/", response_model=User)
def add_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    db_user: User = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user.password = get_password_hash(user.password)
    return create_user(db=db, user=user)


@user_route.get("/users/{user_id}", response_model=User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)) -> User:
    db_user: User = get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not db_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not active")
    return db_user


@user_route.get("/users/", response_model=List[User])
def list_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)) -> list[User]:
    db_user: list[User] = get_users(db=db, skip=skip, limit=limit)
    return db_user


@user_route.put("/users/", response_model=User)
def mod_user(user: UserUpdate, db: Session = Depends(get_db)) -> User:
    db_user: User = get_user_by_email(db=db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not verify_password(plain_password=user.password, hashed_password=db_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    update_data = user.user.dict(exclude_unset=True)
    if update_data["email"]:


        check_email = get_user_email_exclude_id(db=db, user_id=db_user.id, email=update_data["email"])
        print(check_email)
        if check_email:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email already registered")

    update_user(db=db, user_id=db_user.id, user=update_data)

    return get_user(db=db, user_id=db_user.id)


@user_route.delete("/users/")
def delete_user(user: UserDelete, db: Session = Depends(get_db)) -> str:
    db_user = get_user_by_email(db=db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not verify_password(plain_password=user.password, hashed_password=db_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    del_user(db=db, email=user.email)
    return "msg: User deleted successfully"
