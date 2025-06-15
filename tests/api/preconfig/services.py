import uuid
from typing import Annotated

from fastapi import Depends
from fastauth.services import BaseAuthService, UUIDMixin
from fastauth.storage.jwt import JWTTokenStorage
from .models import User
from .repositories import UserRepoDep, OAuthRepoDep
from .config import settings


class AuthService(UUIDMixin, BaseAuthService[User, uuid.UUID]):
    pass


async def get_token_storage():
    return JWTTokenStorage(settings)


async def get_auth_service(
    user_repo: UserRepoDep,
    oauth_repo: OAuthRepoDep,
    token_storage: JWTTokenStorage = Depends(get_token_storage),
):
    return AuthService(settings, user_repo, token_storage, oauth_repo=oauth_repo)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
