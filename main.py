from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.models import Task, User
from app.backend.db import Base, engine, SessionLocal
from app.routers import user

app = FastAPI()

import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Зависимость для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Включение маршрутов пользователя
app.include_router(user.router, prefix="/users", tags=["users"])

# При запуске приложения через main.py будут автоматически созданы таблицы tasks и users в базе данных taskmanager.db

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

