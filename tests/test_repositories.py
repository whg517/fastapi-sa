"""test repositories"""
import pytest
from sqlalchemy import func, select

from tests.example.db import User, UserCreate
from tests.example.repositories import UserRepository


@pytest.fixture()
def repo():
    """repo"""
    return UserRepository()


@pytest.mark.asyncio
async def test_get_all(session, init_user, repo):
    """test get all"""
    objs = await repo.get_all()
    length = await session.scalar(select(func.count()).select_from(User))
    assert len(objs) == length


@pytest.mark.asyncio
async def test_create(session, repo):
    """test create"""
    await repo.create(UserCreate(name='foo', age=10))
    objs = await repo.get_all()
    assert len(objs) == 1
