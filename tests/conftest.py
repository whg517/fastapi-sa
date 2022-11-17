"""Test config"""
import os
from pathlib import Path

import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from starlette.testclient import TestClient

from fastapi_sa.database import db
from tests.example.app import app, settings
from tests.example.db import Base, User


@pytest.fixture()
def db_url():
    """db url"""
    return settings.get('database')


@pytest.fixture()
def user():
    """user"""
    return User


@pytest.fixture(autouse=True, name='migrate')
async def migrate_fixture(db_url):
    """migrate fixture"""
    os.makedirs(Path(db_url.split('///')[1]).parent, exist_ok=True)
    _engine = create_async_engine(db_url)
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await _engine.dispose()


@pytest.fixture(autouse=True)
async def db_init(db_url):
    """db_init"""
    db.init(db_url)


@pytest.fixture()
def db_session_ctx():
    """db session context"""
    token = db.set_session_ctx()
    yield
    db.reset_session_ctx(token)


@pytest.fixture()
async def session(db_session_ctx):
    """session fixture"""
    async with db.session.begin():
        yield db.session


@pytest.fixture()
async def init_user(migrate, user):
    """init_file_record"""
    users = [
        user(name='aoo', age=30),
        user(name='boo', age=20),
        user(name='coo', age=10),
    ]
    async with db():
        db.session.add_all(users)
        await db.session.flush()


@pytest.fixture(name='client')
def create_client():
    """client"""
    with TestClient(app) as cli:
        yield cli
