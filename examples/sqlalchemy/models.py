from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column
from fastauth.contrib.sqlalchemy import (
    BaseUUIDUserModel,
    BaseIntPermissionModel,
    BaseIntRoleModel,
    RBACMixin,
    BaseUserRoleRel,
    BaseRolePermissionRel,
    BaseUUIDOAuthAccount,
    OAuthMixin,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship
import uuid
from fastauth.contrib.sqlalchemy._generic import GUID


class Model(DeclarativeBase):
    pass


class Permission(BaseIntPermissionModel, Model):
    pass


class Role(BaseIntRoleModel[Permission], Model):
    permissions: Mapped[list[Permission]] = relationship(
        secondary="role_permission_rel", lazy="selectin"
    )


class OAuthAccount(BaseUUIDOAuthAccount, Model):
    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID, ForeignKey("users.id", ondelete="CASCADE")
    )


class User(BaseUUIDUserModel, RBACMixin[Role], OAuthMixin[OAuthAccount], Model):
    roles: Mapped[list[Role]] = relationship(secondary="user_role_rel", lazy="selectin")
    oauth_accounts: Mapped[list[OAuthAccount]] = relationship(lazy="joined")


# Need to create many-to-many between users and roles tables
class UserRoleRel(BaseUserRoleRel[uuid.UUID, int], Model):
    pass


# Need to create many-to-many between roles and permissions tables
class RolePermissionRel(BaseRolePermissionRel[int, int], Model):
    pass
