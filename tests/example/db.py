"""db"""
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):  # pylint: disable=too-few-public-methods
    """UserModel"""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    age = Column(Integer)


class UserSchema(BaseModel):  # pylint: disable=too-few-public-methods
    """user schema"""
    id: int
    name: str
    age: int

    class Config:  # pylint: disable=too-few-public-methods
        """config"""
        orm_mode = True


class UserCreate(BaseModel):  # pylint: disable=too-few-public-methods
    """user create"""
    name: str
    age: int
