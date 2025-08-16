from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from routers import user
from backend.db import engine, Base

from routers import task

# создаем сущность FastAPI()
app = FastAPI()
info_ed = ('<h2>Домашнее задание по теме "Использование БД в маршрутизации. 1.1"<br>'
           '<h3>Цель: научиться управлять записями в БД используя SQLAlchemy и маршрутизацию FastAPI.'
           '<br>Задача "Маршрутизация пользователя":'
           '<br>Студентка Екатерина Укладникова'
           '<br>Дата: 10.08.2025 г.</h3>')

# после активации виртуального окружения (в терминале: myenv\\Scripts\\activate) переходим в папку директории проекта: cd app
# запуск сервера: python -m uvicorn main:app

# пишем для сущности FastAPI() маршрут (функцию, которую обрабатывают HTTP-запросы)
@app.get("/")
async def welcome():
    return {"message": "Welcome to Taskmanager"}

@app.get("/info", response_class=HTMLResponse)
async def info():
    return info_ed

# подключаем роутеры
app.include_router(user.router)
app.include_router(task.router)

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

# alembic revision --autogenerate -m "Initial migration"
# python main.py migrate
# alembic upgrade head
# python -m uvicorn main:app
# uvicorn main:app --reload