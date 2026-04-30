from app.core.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


class DatabaseConstructor:
    def __init__(
        self,
        url: str,
        echo: bool,
    ):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

    async def close_connection(self):
        if self.engine is not None:
            return await self.engine.dispose()

    async def get_session(self):
        async with self.session_factory() as session:
            yield session


db_constructor = DatabaseConstructor(
    url=settings.db_url,
    echo=settings.db_echo,
)
