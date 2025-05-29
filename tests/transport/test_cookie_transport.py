from starlette.exceptions import HTTPException
import pytest
from fastapi.security.base import SecurityBase
from fastapi import Request
from fastauth.transport.cookie import CookieTransport


@pytest.fixture
def cookie_settings(mock_settings):
    mock_settings.COOKIE_ACCESS_TOKEN_NAME = "access_token"
    mock_settings.COOKIE_REFRESH_TOKEN_NAME = "refresh_token"
    return mock_settings


@pytest.fixture
def mock_cookie(cookie_settings):
    return CookieTransport(cookie_settings)


def test_cookie_transport_login_response(mock_settings, mock_cookie, mock_payload):
    response = mock_cookie.login_response(mock_payload)
    assert response.status_code == 204
    for header_name, header_value in response.headers.items():
        assert header_name == "set-cookie"
        assert header_value.startswith(
            f"{mock_settings.COOKIE_ACCESS_TOKEN_NAME}={mock_payload.access_token}"
        ) or header_value.startswith(
            f"{mock_settings.COOKIE_REFRESH_TOKEN_NAME}={mock_payload.refresh_token}"
        )


def test_cookie_transport_logout_response(mock_settings, mock_cookie, mock_payload):
    response = mock_cookie.login_response(mock_payload)
    assert response.status_code == 204
    for header_name, header_value in response.headers.items():
        assert header_name == "set-cookie"
        assert header_value.startswith(
            f"{mock_settings.COOKIE_ACCESS_TOKEN_NAME}="
        ) or header_value.startswith(f"{mock_settings.COOKIE_REFRESH_TOKEN_NAME}=")


@pytest.mark.asyncio
async def test_cookie_security_schema(mock_cookie):
    schema = mock_cookie.get_schema()
    assert isinstance(schema, SecurityBase)

    request = Request({"type": "http", "headers": []})
    with pytest.raises(HTTPException, match=r"403"):
        await schema(request)
