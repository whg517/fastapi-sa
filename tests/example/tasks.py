"""tasks"""
from sqlalchemy import select

from fastapi_sa.database import db, session_ctx
from tests.example.db import User, UserSchema


@session_ctx
async def task_get_users():
    """get users"""
    results = await db.session.scalars(select(User))
    objs = [UserSchema.from_orm(i) for i in results.all()]
    return objs


@session_ctx
async def task_get_user_by_id(pk: int):
    """get users"""
    result = await db.session.scalar(select(User).where(User.id == pk))
    return UserSchema.from_orm(result)


@session_ctx
async def task_create_user(name: str, age: int):
    """create user"""
    obj = User(name=name, age=age)
    db.session.add(obj)
    await db.session.flush()
    return UserSchema.from_orm(obj)
