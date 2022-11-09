"""Test config"""
import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from fastapi_sa.database import db
from fastapi_sa.middleware import DBSessionMiddleware


@pytest.fixture(name='db_init')
def db_init():
    """db_init"""
    db.init('sqlite+aiosqlite://')


@pytest.fixture(name='app')
def create_app():
    """create app"""
    return FastAPI()


@pytest.fixture(name='db_session_middleware')
def create_db_session_middleware():
    """DBSessionMiddleware"""
    yield DBSessionMiddleware


@pytest.fixture(name='client')
def create_client(app):
    """client"""
    with TestClient(app) as cli:
        yield cli
