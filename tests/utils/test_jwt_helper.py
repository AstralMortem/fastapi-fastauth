from datetime import timedelta
from time import sleep
import pytest
from fastauth.exceptions import FastAuthException
from fastauth.utils.jwt_helper import JWTPayload, to_jwt_payload, to_jwt_token
from fastauth.utils.time import now


def test_jwt_payload_without_exp():
    now_time = now()
    payload = JWTPayload(sub="test", iat=now_time)

    assert payload.sub == "test"
    assert payload.iat == now_time
    assert payload.exp is None


def test_jwt_payload_with_exp():
    now_time = now()
    payload = JWTPayload(sub="test", iat=now_time, expires_in=100)

    assert payload.iat == now_time
    assert payload.exp == now_time + timedelta(seconds=100)


def test_token_creation():
    secret = "secret"
    now_time = now()

    payload = JWTPayload(sub="test", iat=now_time, expires_in=3600)

    token = payload.to_token(secret)
    assert len(token.split(".")) == 3

    decoded = JWTPayload.from_token(token, secret)

    assert decoded.sub == payload.sub
    assert int(decoded.iat.timestamp()) == int(now_time.timestamp())
    assert int(decoded.exp.timestamp()) == int(payload.exp.timestamp())


def test_token_exception():
    secret = "secret"
    now_time = now()
    payload = JWTPayload(
        sub="test",
        iat=now_time,
        expires_in=3600,
        aud=["test:aud"],
        iss="test",
    )

    token = payload.to_token(secret)

    with pytest.raises(FastAuthException, match=r"400"):
        JWTPayload.from_token(token, secret, audience=["fake:aud"])

    with pytest.raises(FastAuthException, match=r"400"):
        JWTPayload.from_token(token, secret, issuer="fake")

    with pytest.raises(FastAuthException, match=r"400"):
        JWTPayload.from_token(token, "SECRET_INVALID")

    with pytest.raises(FastAuthException, match=r"400"):
        payload.exp = now_time + timedelta(seconds=1)
        sleep(1)
        token = payload.to_token(secret)
        JWTPayload.from_token(token, secret)


def test_shortcuts(mock_settings):
    mock_settings.SECRET_KEY = "SECRET"
    payload = JWTPayload(sub="test")
    token = to_jwt_token(mock_settings, payload)
    decoded_payload = to_jwt_payload(mock_settings, token)
    assert decoded_payload.sub == "test"
