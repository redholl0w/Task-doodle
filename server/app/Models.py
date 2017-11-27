from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    desc = Column(String)


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    done = Column(Boolean, default=False)
    desc = Column(String)
    todo_id = Column(Integer, ForeignKey('todos.id'), nullable=False)

    user = relationship('Todo')


engine = create_engine('sqlite:///todo.db')
Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
