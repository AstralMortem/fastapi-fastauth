from fastapi import FastAPI
from preconfig.db_session import engine
from preconfig.models import Model
from preconfig.router import router
from fastapi.testclient import TestClient
import pytest


@pytest.fixture(scope="session")
async def test_app():
    app = FastAPI()
    app.include_router(router)
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    yield app
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


@pytest.fixture
def client(test_app):
    return TestClient(test_app)
