from fastauth.schemas.auth import TokenData, TokenType
from fastauth.storage import JWTTokenStorage
import pytest


@pytest.fixture
def mock_storage(mock_settings):
    return JWTTokenStorage(mock_settings)


@pytest.fixture
def token_data():
    return TokenData(
        user_id="test",
        email="email",
        roles=["TEST_ROLE"],
        permissions=["TEST_PERMISSION"],
        token_type=TokenType.ACCESS,
        expires_in=3600,
        jti="jti",
    )


def test_encode_token(mock_storage, token_data):
    token = mock_storage.encode_token(token_data)
    assert len(token.split(".")) == 3


def test_decode_token(mock_storage, token_data):
    token = mock_storage.encode_token(token_data)
    decoded_token = mock_storage.decode_token(token)
    assert decoded_token.user_id == "test"
    assert decoded_token.email == "email"
    assert decoded_token.roles == ["TEST_ROLE"]
    assert decoded_token.permissions == ["TEST_PERMISSION"]
    assert decoded_token.expires_in is None  # 3600
    assert decoded_token.jti == "jti"
    assert decoded_token.token_type == TokenType.ACCESS
