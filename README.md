# fastapi-sa

![GitHub](https://img.shields.io/github/license/whg517/aio-pydispatch?style=flat-square)
![PyPI](https://img.shields.io/pypi/v/0.0.1?color=blue&label=pypi&logo=fastapi_sa)

fastapi-sa provides a simple integration between FastAPI and SQLAlchemy in your application.
you can use decorators or middleware to transaction management.

## Installing

install and update using pip:

```shell
$ pip install fastapi-sa
```

## Examples

### Create models for examples, `models.py`

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Item(Base):
    """ItemModel"""
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

```

### Usage fastapi middleware

```python
from fastapi import FastAPI
from fastapi_sa.database import db
from fastapi_sa.middleware import DBSessionMiddleware

from models import Item

app = FastAPI()
db.init(url="sqlite://")
app.add_middleware(DBSessionMiddleware)


@app.put("/items")
async def get_users(name: str):
    async with db() as session:
        item = Item(name=name)
        session.add(item)
    return {'msg': 'ok'}
```

### Usage other asynchronous database operations

```python
import asyncio
from fastapi_sa.database import db, session_ctx

from models import Item

db.init(url="sqlite://")


@session_ctx
async def add_data(name: str):
    async with db() as session:
        item = Item(name=name)
        session.add(item)


asyncio.run(add_data('item_test'))
```

## Similar design

- [FastAPI-SQLAlchemy](https://github.com/mfreeborn/fastapi-sqlalchemy)

## Based on
- [FastAPI](https://github.com/tiangolo/fastapi)
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)

## Develop

You may need to read the [develop document](./docs/development.md) to use SRC Layout in your IDE.

