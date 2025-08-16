# Домашнее задание по теме "Использование БД в
# маршрутизации. 1.2".
# Цель: закрепить навык управления записями в БД, используя
# SQLAlchemy и маршрутизацию FastAPI.
# Задача "Маршрутизация заданий":
# Необходимо описать логику функций в task.py, используя ранее
# написанные маршруты FastAPI.

from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated

from models.task import Task

from schemas import CreateUser, UpdateUser, CreateTask, UpdateTask
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify

router = APIRouter(prefix="/task", tags=["task"])

@router.get("/all_tasks", summary="Receive all tasks")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks

@router.get("/task_id")
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found')
    return task

# к нашему роутеру коннектим блок, который будет позволять добавлять новые элементы:
@router.post("/create")
async def create_task(user_id: int, new_user: CreateUser, new_task: CreateTask, db: Annotated[Session, Depends(get_db)]):
    slug = slugify(new_task.title)
    task_data = new_task.dict()
    task_data['slug'] = slug
    query = select(Task).where(Task.id == user_id)
    user = db.scalar(query)
    if user:
        db.execute(insert(Task).where(Task.id == user_id).values(**new_task.dict()))
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "User update is successful!"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User was not found")

@router.put("/update")
async def update_task():
    pass
@router.delete("/delete")
async def delete_task():
    pass