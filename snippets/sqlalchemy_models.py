# --8<-- [start:user]
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from fastauth.contrib.sqlalchemy import BaseUUIDUserModel

class Base(DeclarativeBase):
    pass


class User(BaseUUIDUserModel, Base):
    pass

# --8<-- [end:user]

# --8<-- [start:rbac]

from fastauth.contrib.sqlalchemy import BaseIntRoleModel, BaseIntPermissionModel, BaseRolePermissionRel

class Permission(BaseIntPermissionModel, Base):
    pass


class Role(BaseIntRoleModel[Permission], Base):
    permisions: Mapped[Permission] = relationship(lazy='selectin')


# Need for sqlalchemy, to indentify many-to-many table
class RolePermissionRel(BaseRolePermissionRel[int, int], Base):
    pass

# --8<-- [end:rbac]


# --8<-- [start:rbac-user]
from fastauth.contrib.sqlalchemy import BaseUUIDUserModel, RBACMixin, BaseUserRoleRel
import uuid

class User(BaseUUIDUserModel,RBACMixin[Role], Base):
    roles: Mapped[Role] = relationship(lazy="selectin")


# Need for sqlalchemy, to indentify many-to-many table
class UserRoleRel(BaseUserRoleRel[uuid.UUID, int], Base):
    pass

# --8<-- [end:rbac-user]

# --8<-- [start:oauth]
from fastauth.contrib.sqlalchemy import BaseUUIDOAuthAccount

class OAuthAccount(BaseUUIDOAuthAccount):
    pass

# --8<-- [end:oauth]


# --8<-- [start:oauth-user]
from fastauth.contrib.sqlalchemy import BaseUUIDUserModel, RBACMixin, OAuthMixin
import uuid

class User(BaseUUIDUserModel,RBACMixin[Role], OAuthMixin[OAuthAccount], Base):
    roles: Mapped[Role] = relationship(lazy="selectin")
    oauth_accounts: Mapped[OAuthAccount] = relationship(lazy="joined")

# --8<-- [end:oauth-user]