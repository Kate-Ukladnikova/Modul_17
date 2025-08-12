# Домашнее задание по теме "Структура проекта.
# Маршруты и модели Pydantic."
# Цель: усвоить основные правила структурирования проекта с
# использованием FastAPI. Начать написание небольшого "API" для
# менеджмента задач пользователей.
# Задача "Основные маршруты".
# Создадим объект APIRouter, позволяющий разнести маршруты по модулям:

from fastapi import APIRouter
router = APIRouter(prefix="/task", tags=["task"])

@router.get("/")
async def all_tasks():
    pass
@router.get("/task_id")
async def task_by_id():
    pass
# к нашему роутеру коннектим блок, который будет позволять добавлять новые элементы:
@router.post("/create")
async def create_task():
    pass

@router.put("/update")
async def update_task():
    pass
@router.delete("/delete")
async def delete_task():
    pass