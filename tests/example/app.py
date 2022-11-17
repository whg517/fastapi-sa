"""app"""

from fastapi import Depends, FastAPI

from fastapi_sa.middleware import DBSessionMiddleware
from tests.example.db import UserCreate
from tests.example.repositories import UserRepository

settings = {
    'database': 'sqlite+aiosqlite:////tmp/test.db',
}

app = FastAPI()
app.add_middleware(DBSessionMiddleware)


@app.get('/users')
async def get_all(repo: UserRepository = Depends()):
    """get all users"""
    return await repo.get_all()


@app.post('/users')
async def create(
        obj_in: UserCreate,
        repo: UserRepository = Depends()
):
    """create a new user"""
    return await repo.create(obj_in)
