# Домашнее задание по теме "Модели SQLALchemy.
# Отношения между таблицами.
# Цель: усвоить основные правила структурирования проекта с использованием
# FastAPI. Научиться создавать модели баз данных, используя SQLAlchemy.
# Задача "Модели SQLAlchemy".
# Необходимо создать 2 модели для базы данных, используя SQLAlchemy.
# База данных и движок:

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from sqlalchemy import Column, Integer, String

# Cоздаю движок, указав путь в БД - 'sqlite:///taskmanager.db' и локальную сессию:
engine = create_engine("sqlite:///taskmanager.db", echo = True)
SessionLocal = sessionmaker(bind=engine)

# Cоздаю базовый класс Base для других моделей:
class Base(DeclarativeBase):
    pass