from sqlalchemy import Table, Column, Integer, String, Date, Enum, Text, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func

from datetime import datetime
import uuid
import enum


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


association_table = Table(
    'developer_project_association',
    Base.metadata,
    Column('developer_id', Integer, ForeignKey('developers.id', ondelete='CASCADE')),
    Column('project_id', Integer, ForeignKey('projects.id', ondelete='CASCADE'))
)


class Status(enum.Enum):
    pending = 'Ожидание'
    in_progress = 'В процессе'
    canceled = 'Отмененный'
    completed = 'Завершен'

    def next(self):
        cls = self.__class__
        members = list(cls)
        index = members.index(self) + 1
        if index >= len(members):
            index = 0
        return members[index]

class DeveloperSpecialties(enum.Enum):
    backend = 'Бэкэнд'
    frontend = 'Фронтэнд'
    unchosen = 'Не выбрано'

    def next(self):
        cls = self.__class__
        members = list(cls)
        index = members.index(self) + 1
        if index >= len(members):
            index = 0
        return members[index]

class Developer(Base):
    __tablename__ = "developers"

    id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(BigInteger, unique=True)
    username = Column(String, nullable=True)
    first_name = Column(String)
    specialty = Column(Enum(DeveloperSpecialties), default=DeveloperSpecialties.unchosen)
    projects = relationship(
        "Project", 
        secondary=association_table, 
        back_populates="developers", 
        cascade="save-update, merge")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, unique=True)
    title = Column(String, unique=True)
    description = Column(Text, nullable=True)
    price = Column(Integer)
    status = Column(Enum(Status), default=Status.pending)
    taken_at = Column(Date, nullable=True)
    developer_count = Column(Integer, default=1)
    developers = relationship(
        "Developer", 
        secondary=association_table, 
        back_populates="projects",
        cascade="save-update, merge")


class AuthKey(Base):
    __tablename__ = 'auht_key'

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, nullable=False)  # Поле для хранения ключа

