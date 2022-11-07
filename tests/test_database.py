"""
test database
"""
import asyncio

import pytest

from fastapi_sa.database import db


@pytest.fixture
def db_init():
    """db_init"""
    db.init('sqlite+aiosqlite://')


async def test_session_ctx(db_init):
    """test session ctx"""

    async def foo():
        """foo"""
        return db.session

    async with db() as session:
        result = await foo()
        assert id(result) == id(session)
        result = await asyncio.create_task(foo())
        assert id(result) == id(session)
