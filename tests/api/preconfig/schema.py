from fastauth.schemas.users import BaseUserCreate, BaseUserRead, BaseUserUpdate
import uuid


class UserRead(BaseUserRead[uuid.UUID]):
    pass


class UserCreate(BaseUserCreate):
    pass


class UserUpdate(BaseUserUpdate):
    pass
