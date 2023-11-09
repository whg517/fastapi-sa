"""repository"""
from sqlalchemy import select

from fastapi_sa.database import db
from tests.example.db import User, UserCreate, UserSchema


class UserRepository:
    """user repository"""

    @property
    def model(self):
        """model"""
        return User

    async def get_all(self):
        """get all"""
        result = await db.session.scalars(select(self.model))
        objs = [UserSchema.model_validate(i) for i in result.all()]
        return objs

    async def create(self, obj_in: UserCreate):
        """create"""
        obj = self.model(**obj_in.model_dump())
        db.session.add(obj)
        await db.session.flush()
        return UserSchema.model_validate(obj)
