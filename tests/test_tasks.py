"""test tasks"""
import pytest
from pydantic import ValidationError

from tests.example.db import User
from tests.example.tasks import task_create_user, task_get_users


@pytest.mark.asyncio
async def test_get_users(init_user):
    """test get users"""
    users = await task_get_users()
    assert len(users) == 3


@pytest.mark.asyncio
async def test_create_user(session):
    """test create user"""
    obj = await task_create_user('doo', 12)
    user = await session.get(User, obj.id)
    assert user.name == obj.name


@pytest.mark.asyncio
async def test_create_user_rollback(init_user):
    """test create user rollback"""
    with pytest.raises(ValidationError):
        await task_create_user('doo', 'age')  # noqa
    users = await task_get_users()
    assert len(users) == 3
