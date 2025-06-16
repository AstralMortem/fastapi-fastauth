from preconfig.schema import UserCreate, UserRead
from preconfig.config import settings

from fastauth.routes import get_signup_router
from preconfig.security import security
import pytest
from unittest.mock import patch


@pytest.mark.asyncio
async def test_user_safe_signup(client):
    payload = UserCreate(
        email="test@example.com",
        password="test",
        is_active=True,
        is_verified=True,
        roles=["USER"],
    )
    response = await client.post("/api/auth/signup", json=payload.model_dump())
    assert response.status_code == 200

    user = UserRead.model_validate(response.json())
    assert user.email == "test@example.com"
    assert user.is_active == settings.DEFAULT_USER_IS_ACTIVE
    assert user.is_verified == settings.DEFAULT_USER_IS_VERIFIED


# @pytest.mark.asyncio
# async def test_user_unsafe_signup(client):

#     with patch('preconfig.router.router') as router:
#         router.return_value = get_signup_router(security, UserCreate, UserRead, False)

#         payload = UserCreate(email="test2@example.com", password="test", is_active=True, is_verified=True, roles=['USER'])
#         response = await client.post('/api/auth/signup', json=payload.model_dump())
#         assert response.status_code == 200

#         user = UserRead.model_validate(response.json())
#         assert user.email == "test2@example.com"
#         assert user.is_active is True
#         assert user.is_verified is True
