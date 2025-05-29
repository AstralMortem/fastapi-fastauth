from fastauth.transport.bearer import BearerTransport
from fastapi.security.base import SecurityBase
from fastapi import Request
from starlette.exceptions import HTTPException
import pytest
import ast


@pytest.fixture
def mock_bearer(mock_settings) -> BearerTransport:
    return BearerTransport(mock_settings)


def test_login_response(mock_bearer, mock_payload):
    response = mock_bearer.login_response(mock_payload)
    assert response.status_code == 200
    d = ast.literal_eval(response.body.decode("utf8"))
    assert d["access_token"] == mock_payload.access_token
    assert d["refresh_token"] == mock_payload.refresh_token


def test_logout_response(mock_bearer):
    response = mock_bearer.logout_response()
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_security_schema(mock_bearer):
    schema = mock_bearer.get_schema()

    assert isinstance(schema, SecurityBase)

    request = Request({"type": "http", "headers": []})
    with pytest.raises(HTTPException, match=r"401"):
        await schema(request)
