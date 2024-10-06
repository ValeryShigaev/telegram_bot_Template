import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    f'{os.environ.get("DIALECT")}+{os.environ.get("DRIVER")}://'
    f'{os.environ.get("POSTGRES_USER")}:{os.environ.get("POSTGRES_PASSWORD")}'
    f'@db:{os.environ.get("PORT")}/{os.environ.get("POSTGRES_DB")}',
    echo=False)

Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_session() -> AsyncSession:
    async with Session() as s:
        try:
            yield s
        finally:
            await s.close()
