from fastapi import FastAPI
import pytest
from preconfig.models import Model, Role
from preconfig.router import router
from preconfig.config import settings
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from preconfig.db_session import get_session
import pytest_asyncio

engine = create_async_engine('sqlite+aiosqlite:///:memory:', echo=True)
session_factory = async_sessionmaker(engine, expire_on_commit=True)

@pytest_asyncio.fixture()
async def get_test_session():
    async with session_factory() as session:
        yield session

@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

    async with session_factory() as session:
        for role_name in settings.DEFAULT_USER_ROLES:
            session.add(Role(name=role_name))
        await session.commit()

    yield
    # Optional: Drop tables after tests
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


@pytest.fixture()
def test_app():
    app = FastAPI()
    app.include_router(router)
    return app


@pytest_asyncio.fixture()
async def client(test_app, get_test_session):
    
    test_app.dependency_overrides[get_session] = lambda: get_test_session

    async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test") as ac:
        yield ac

    test_app.dependency_overrides.clear()

