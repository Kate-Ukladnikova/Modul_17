# Модели баз данных

from backend.db import Base

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.schema import CreateTable

# from Modul_17.app.models import User

# после активации виртуального окружения (в терминале: myenv\\Scripts\\activate) переходим в папку директории проекта: cd app
from slugify import slugify


class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key = True, index=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer, default = None)
    completed = Column(Boolean, default = False)
    # user_id - целое число, внешний ключ на id из таблицы 'users' (Внешний ключ к users.id),
    # не NULL, с индексом
    user_id = Column(Integer, ForeignKey('users.id'), nullable = True, index=True)
    slug = Column(String, unique=True, index=True)

    user = relationship("User", back_populates="tasks")

print(CreateTable(Task.__table__))

