from typing import Annotated
from fastapi import Depends
from fastauth.repositories import IRoleRepository

from .models import OAuthAccount, User, Role
from fastauth.contrib.sqlalchemy import (
    SQLAlchemyUserRepository,
    SQLAlchemyOAuthRepository,
    SQLAlchemyRoleRepository
)
import uuid
from .db_session import SessionDep


class UserRepository(SQLAlchemyUserRepository[User, uuid.UUID]):
    model = User


class RoleRepository(SQLAlchemyRoleRepository[Role, int]):
    model = Role

class OAuthRepository(SQLAlchemyOAuthRepository[OAuthAccount, uuid.UUID, User]):
    model = OAuthAccount
    user_model = User


async def get_user_repository(session: SessionDep):
    return UserRepository(session)


async def get_oauth_repository(session: SessionDep):
    return OAuthRepository(session)

async def get_role_repository(session: SessionDep):
    return RoleRepository(session)

UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]
OAuthRepoDep = Annotated[OAuthRepository, Depends(get_oauth_repository)]
RoleRepoDep = Annotated[IRoleRepository, Depends(get_role_repository)]