from fastauth.services import BaseAuthService
from fastapi import Depends
from typing import Annotated

class AuthService(BaseAuthService):
    pass


async def get_auth_service(
    user_repo: UserRepoDep,
    oauth_repo: OAuthRepoDep,
    role_repo: RoleRepoDep,
    token_storage: JWTTokenStorage = Depends(get_token_storage),
):
    return AuthService(
        settings, user_repo, token_storage, oauth_repo=oauth_repo, role_repo=role_repo
    )


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
