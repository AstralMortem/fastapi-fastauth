import pytest
from fastauth.schemas.auth import TokenResponse


@pytest.fixture(autouse=True)
def mock_payload():
    return TokenResponse(
        access_token="access_token",
        refresh_token="refresh_token",
        expires_in=3600,
    )
