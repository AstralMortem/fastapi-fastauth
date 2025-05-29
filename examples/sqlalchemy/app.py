from contextlib import asynccontextmanager

from fastapi import FastAPI
from router import router
from config import settings
import uvicorn
from fastauth.exceptions import set_exception_handler
from db_session import engine, session_factory
from models import Model, User
from fastauth.utils.password import PasswordHelper


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

    user = User(email="string", hashed_password=PasswordHelper().hash("string"))
    async with session_factory() as session:
        session.add(user)
        await session.commit()

    yield
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


app = FastAPI(lifespan=lifespan)


set_exception_handler(app, settings.DEBUG)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app)
