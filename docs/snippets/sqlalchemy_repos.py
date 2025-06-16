# --8<-- [start:repos]
from fastauth.repositories import IRoleRepository, IUserRepository, IOAuthRepository
from fastauth.contrib.sqlalchemy import (
    SQLAlchemyUserRepository,
    SQLAlchemyOAuthRepository,
    SQLAlchemyRoleRepository,
)
import uuid



class UserRepository(SQLAlchemyUserRepository[User, uuid.UUID]):
    model = User


class RoleRepository(SQLAlchemyRoleRepository[Role, int]):
    model = Role


class OAuthRepository(SQLAlchemyOAuthRepository[OAuthAccount, uuid.UUID, User]):
    model = OAuthAccount
    user_model = User

# --8<-- [end:repos]

# --8<-- [start:deps]
from fastapi import Depends
from typing import Annotated

async def get_user_repository(session: SessionDep):
    return UserRepository(session)


async def get_oauth_repository(session: SessionDep):
    return OAuthRepository(session)


async def get_role_repository(session: SessionDep):
    return RoleRepository(session)


UserRepoDep = Annotated[IUserRepository, Depends(get_user_repository)]
OAuthRepoDep = Annotated[IOAuthRepository, Depends(get_oauth_repository)]
RoleRepoDep = Annotated[IRoleRepository, Depends(get_role_repository)]

# --8<-- [end:deps]