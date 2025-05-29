import pytest
from fastauth.settings import FastAuthSettings


@pytest.fixture(scope="function", autouse=True)
def mock_settings():
    return FastAuthSettings()
