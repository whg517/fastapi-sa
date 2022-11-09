"""
test middleware
"""
from starlette.middleware.base import BaseHTTPMiddleware

from fastapi_sa.database import db


def test_init_db_session_middleware(app, db_session_middleware):
    """test db session middleware type"""
    db_session_middleware_obj = db_session_middleware(app)
    assert isinstance(db_session_middleware_obj, BaseHTTPMiddleware)


async def test_inside_route(app, db_init, client, db_session_middleware):
    """test inside route"""
    app.add_middleware(db_session_middleware)

    @app.get("/")
    async def test_get():
        async with db() as session:
            assert id(db.session) == id(session)

    client.get("/")


async def test_outside_of_route(db_init):
    """test outside route"""
    async with db() as session:
        assert id(db.session) == id(session)
