"""
database
"""
import contextvars
import logging
from typing import cast

import sqlalchemy as sa
import sqlalchemy.orm  # pylint: disable=unused-import
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from fastapi_sa.exceptions import SQLAlchemyNotInitError

logger = logging.getLogger(__name__)


class SingleMeta(type):
    """
    单例元类
    """
    __instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.__instance:
            instance = super().__call__(*args, **kwargs)
            cls.__instances = instance
        return cls.__instances


class Database(metaclass=SingleMeta):
    """
    Database with Sqlalchemy

    usage:
        >>> db.init('sqlite+aiosqlite://')
    """

    def __init__(self):
        self.__engine: sa.ext.asyncio.engine.AsyncEngine | None = None
        self.__session_maker: sa.orm.sessionmaker | None = None
        self.__session_ctx: contextvars.ContextVar[
            sa.ext.asyncio.session.AsyncSession | None
            ] = contextvars.ContextVar("session_ctx", default=None)

    def init(
            self,
            url: str,
            echo: bool = False
    ):
        """

        :param url:
        :param echo:
        :return:
        """
        self.__engine = create_async_engine(
            url,
            echo=echo,
            future=True,
        )
        self.__session_maker = sa.orm.sessionmaker(
            self.engine,
            class_=sa.ext.asyncio.session.AsyncSession,
            # expire_on_commit=False,  # 取消提交后过期操作，此现象会产生缓存，请注意清理。
        )

    @property
    def session_ctx(self):
        """session context var"""
        return self.__session_ctx

    @property
    def session_maker(self):
        """sqlalchemy session maker"""
        if self.__session_maker:
            return self.__session_maker
        raise SQLAlchemyNotInitError

    @property
    def engine(self):
        """sqlalchemy engine"""
        if self.__engine:
            return self.__engine
        raise SQLAlchemyNotInitError

    @property
    def session(self) -> AsyncSession:
        """
        sqlalchemy session.

        You should call `db.init` first.
        :return:
        """
        assert self.session_maker
        _session = self.__session_ctx.get()
        if not _session:
            _session = self.session_maker()
        return _session

    def __call__(self, **session_args):
        return _Session(self, session_args)


class _Session:
    def __init__(self, sa_db, session_args):
        self._sa_db = sa_db
        self._session_args = session_args
        self.__session_ctx_token = None

    async def __aenter__(self):
        """"""
        assert self._sa_db.session_maker
        _session = self._sa_db.session_maker(**self._session_args)
        _session = cast(AsyncSession, _session)
        logger.debug('Init context session, session id: %d', id(_session))
        self.__session_ctx_token = self._sa_db.session_ctx.set(_session)
        logger.debug(
            'Set session %d to context var, context var token: %s',
            id(_session), self.__session_ctx_token
        )
        return _session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        _session = self._sa_db.session_ctx.get()
        if exc_type is not None:
            await _session.rollback()
        session_id = id(_session)
        await _session.commit()
        await _session.close()
        self._sa_db.session_ctx.reset(self.__session_ctx_token)
        logger.debug(
            'Reset context var token %s, and session id: %d',
            self.__session_ctx_token, id(session_id)
        )


db = Database()


def session_ctx(func: callable):
    """
    Session ctx with decorator

    usage:
        >>> @session_ctx
            async def foo():
                obj = await db.session.get(User, 1)
                assert obj.id == 1
    """

    async def _wrap(*args, **kwargs):
        async with db():
            result = await func(*args, **kwargs)
            return result

    return _wrap
