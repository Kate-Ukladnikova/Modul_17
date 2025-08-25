# Домашнее задание по теме "Использование БД в
# маршрутизации. 1.2".
# Цель: закрепить навык управления записями в БД, используя
# SQLAlchemy и маршрутизацию FastAPI.
# Задача "Маршрутизация заданий":
# Необходимо описать логику функций в task.py, используя ранее
# написанные маршруты FastAPI-.

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

from models.user import User

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
            detail='User was not found')
    return task

# к нашему роутеру коннектим блок, который будет позволять добавлять новые элементы:
@router.post("/create")
async def create_task(create_tasks: CreateTask, user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

    new_task = Task(
        priority=0,
        user_id=user_id,
        content=create_tasks.content,
        title=create_tasks.title,
        completed=False,
        slug=slugify(create_tasks.title)
    )

    db.add(new_task)
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put("/update")
async def update_task(task_id: int, update_task: UpdateTask, db: Annotated[Session, Depends(get_db)]):
    query = select(Task).where(Task.id == task_id)
    task = db.scalar(query)
    if task:
        db.execute(update(User).where(Task.id == task_id).values(**update_task.dict()))
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "Task update is successful!"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task was not found")

@router.delete("/delete")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    query = select(User).where(Task.id == task_id)
    task = db.scalar(query)
    if task:
        db.execute(delete(Task).where(Task.id == task_id))
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "Task deletion successful!"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task was not found")