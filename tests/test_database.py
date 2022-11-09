"""
test database
"""
import asyncio

from fastapi_sa.database import db


async def test_session_ctx(db_init):
    """test session ctx"""

    async def task():
        """foo"""
        return db.session

    async with db() as session:
        result = await task()
        assert id(result) == id(session)
        result = await asyncio.create_task(task())
        assert id(result) == id(session)
