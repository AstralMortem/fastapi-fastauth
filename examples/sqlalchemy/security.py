from fastauth import FastAuth
from config import settings
from services import get_auth_service
from fastauth.transport import BearerTransport

transport = BearerTransport(settings)
security = FastAuth(settings, get_auth_service, transport)
