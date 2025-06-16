from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with session_factory() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


SessionDep = Annotated[AsyncSession, Depends(get_session)]
