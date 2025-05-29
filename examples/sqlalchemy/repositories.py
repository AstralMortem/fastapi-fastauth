from typing import Annotated
from fastapi import Depends

from examples.sqlalchemy.models import OAuthAccount
from fastauth.contrib.sqlalchemy import (
    SQLAlchemyUserRepository,
    SQLAlchemyOAuthRepository,
)
from models import User
import uuid
from db_session import SessionDep


class UserRepository(SQLAlchemyUserRepository[User, uuid.UUID]):
    model = User


class OAuthRepository(SQLAlchemyOAuthRepository[OAuthAccount, uuid.UUID, User]):
    model = OAuthAccount
    user_model = User


async def get_user_repository(session: SessionDep):
    return UserRepository(session)


async def get_oauth_repository(session: SessionDep):
    return OAuthRepository(session)


UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]
OAuthRepoDep = Annotated[OAuthRepository, Depends(get_oauth_repository)]
