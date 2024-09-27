from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import User
from app.schemans import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter()

# Возвращает список всех пользователей
@router.get("/")
def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users

# Возвращает пользователя по ID или выбрасывает исключение, если пользователь не найден
@router.get("/{user_id}")
def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is not None:
        return user
    raise HTTPException(status_code=404, detail="User was not found")

# Создает нового пользователя, используя данные из модели CreateUser. Обрабатывает возможные исключения.
@router.post("/create")
def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    try:
        new_user = insert(User).values(
            username=user.username,
            firstname=user.firstname,
            lastname=user.lastname,
            age=user.age,
            slug=slugify(user.username)
        )
        db.execute(new_user)
        db.commit()
        return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"User creation failed: {str(e)}")

# Обновляет данные пользователя по ID, используя данные из модели UpdateUser
@router.put("/update/{user_id}")
def update_user(user_id: int, user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    stmt = update(User).where(User.id == user_id).values(
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age
    )
    result = db.execute(stmt)
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User was not found")
    return {"status_code": status.HTTP_200_OK, "transaction": "User update is successful!"}

# Удаляет пользователя по ID
@router.delete("/delete/{user_id}")
def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    stmt = delete(User).where(User.id == user_id)
    result = db.execute(stmt)
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User was not found")
    return {"status_code": status.HTTP_200_OK, "transaction": "User deletion is successful!"}