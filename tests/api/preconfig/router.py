from fastauth.routes.auth import get_auth_router
from fastauth.routes.users import get_users_router
from fastauth.routes.signup import get_signup_router
from fastauth.routes.password_reset import get_reset_password_router
from fastauth.routes.verification import get_verification_router

from .security import security
from fastapi import APIRouter
from .schema import UserRead, UserCreate, UserUpdate

router = APIRouter(prefix="/api")

router.include_router(get_auth_router(security))
router.include_router(get_users_router(security, UserRead, UserUpdate))
router.include_router(get_signup_router(security, UserCreate, UserRead))
router.include_router(get_reset_password_router(security))
router.include_router(get_verification_router(security, UserRead))

# github_client = GitHubOAuth2("GITHUB_CLIENT_ID", "GITHUB_CLIENT_SECRET")
# router.include_router(get_oauth_router(security, github_client))
