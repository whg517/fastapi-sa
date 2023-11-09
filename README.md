# fastapi-sa

[![GitHub Workflow Status (branch)](https://github.com/crawlerstack/fastapi-sa/workflows/main/badge.svg?event=push&branch=main)](https://github.com/crawlerstack/fastapi-sa/actions?query=workflow%3Amain+event%3Apush+branch%3Amain)
![GitHub](https://img.shields.io/github/license/whg517/fastapi-sa?style=flat-square)
![Python](https://img.shields.io/pypi/pyversions/fastapi-sa)
![PyPI](https://img.shields.io/pypi/v/fastapi-sa?style=flat-square)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/c76cfa7d7d274f899967019900465403)](https://www.codacy.com/gh/whg517/fastapi-sa/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=whg517/fastapi-sa&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/whg517/fastapi-sa/graph/badge.svg?token=F098K6GGGC)](https://codecov.io/gh/whg517/fastapi-sa)

fastapi-sa provides a simple integration between FastAPI and SQLAlchemy in your application.
you can use decorators or middleware to transaction management.

## Installing

install and update using pip:

```shell
pip install fastapi-sa
```

## Examples

### Create models for examples, `models.py`

```python
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    """UserModel"""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    age = Column(Integer)


class UserSchema(BaseModel):
    """user schema"""
    id: int
    name: str
    age: int

    class Config:
        """config"""
        orm_mode = True
```

### Database migrations for examples

code for create tables, also you can use database migrations.

```python
from sqlalchemy import create_engine
from models import Base

engine = create_engine('sqlite+aiosqlite:////tmp/test.db')
Base.metadata.create_all(engine) 
```

### DB init for examples

```python
from fastapi_sa.database import db

db.init(url='sqlite+aiosqlite:////tmp/test.db')
```

### Usage 1: fastapi middleware

```python
from fastapi import FastAPI
from sqlalchemy import select

from fastapi_sa.database import db
from fastapi_sa.middleware import DBSessionMiddleware
from tests.example.db import User, UserSchema

app = FastAPI()
app.add_middleware(DBSessionMiddleware)


@app.get('/users')
async def get_users():
    """get all users"""
    result = await db.session.scalars(select(User))
    objs = [UserSchema.from_orm(i) for i in result.all()]
    return objs
```

### Usage 2: other asynchronous database operations

```python
from sqlalchemy import select

from fastapi_sa.database import db, session_ctx
from tests.example.db import User, UserSchema


@session_ctx
async def get_users():
    """get users"""
    results = await db.session.scalars(select(User))
    objs = [UserSchema.from_orm(i) for i in results.all()]
    return objs
```

### Usage 3: with fixtures in pytest

```python
import pytest
from fastapi_sa.database import db


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
```

If you initialize data in fixture, please use

```python
from fastapi_sa.database import db
from models import User

async with db():
    users = User(name='aoo', age=12)
    db.session.add(users)
    await db.session.flush()
```

if you test class methods, please use

```python
import pytest
from sqlalchemy import func, select
from models import User, UserSchema
from fastapi_sa.database import db


class UserRepository:
    """user repository"""

    @property
    def model(self):
        """model"""
        return User

    async def get_all(self):
        """get all"""
        result = await db.session.scalars(select(self.model))
        objs = [UserSchema.from_orm(i) for i in result.all()]
        return objs


# the test case is as follows    

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
```

## Similar design

- [FastAPI-SQLAlchemy](https://github.com/mfreeborn/fastapi-sqlalchemy)

## Based on

- [FastAPI](https://github.com/tiangolo/fastapi)
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)

## Develop

You may need to read the [develop document](./docs/development.md) to use SRC Layout in your IDE.
