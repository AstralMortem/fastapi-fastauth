# Configuration

First you need to choose orm provider, for this examples we will use SQLAlchemy, and init `FastAuthSettings` class.
Let`s init configuration, which we use later.

``` python
from fastauth.settings import FastAuthSettings

settings = FastAuthSettings()

```

There we can share some variables across classes inside library. Also we can extend or override config variables, for example by direct change, or inherit class.

``` python
from fastauth.settings import FastAuthSettings

class Settings(FastAuthSettings):
    # Override flag to allow inactive users to login
    ALLOW_INACTIVE_USERS: bool = False 

```


## Models

First of all, we need to create tables inside DB, so let`s implement ORM Models class.
FastAuth support sqlalchemy out-the-box, so we just need to inherit ready to use mixins

``` python
--8<-- "docs/snippets/sqlalchemy_models.py:user"
```

!!! tip "Another ID field"
    You can customize User ID field, you need to inherit `BaseUserModel[ID]` class, and set `id` field
    ``` python
    from fastauth.contrib.sqlalchemy import BaseUserModel
    from sqlalchemy.orm import Mapped, mapped_column

    class User(BaseUserModel[int]):
        id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    ```


Now we have `User` model. But if you want add support of RBAC, you need to create `Role` and `Permission` models.
``` python
--8<-- "docs/snippets/sqlalchemy_models.py:rbac"
```

Then we need to upgrade our `User` model and add connection between roles and users tables
``` python
--8<-- "docs/snippets/sqlalchemy_models.py:rbac-user"
```

!!! tip "Role and Permission ID field"
    As for `User` model, you can also customize `Role` and `Permission` id field, by inherit `BaseRoleModel` and `BasePermissionModel`.

    ``` python
    from fastauth.contrib.sqlalchemy import BaseRoleModel, BasePermissionModel
    from sqlalchemy.orm import Mapped, mapped_column
    import uuid

    class Role(BaseRoleModel[uuid.UUID]):
        id: Mapped[uuid.UUID] = mapped_column(primary_key=True, autoincrement=True, default=uuid.uuid4)

    class Permission(BasePermissionModel[uuid.UUID]):
        id: Mapped[uuid.UUID] = mapped_column(primary_key=True, autoincrement=True, default=uuid.uuid4)

    ```

For OAuth support, we need create proper model too.
``` python
--8<-- "docs/snippets/sqlalchemy_models.py:oauth"
```

!!! tip "OAuth ID Field"
    There is we can customize ID field to, just inherit `BaseOAuthModel` class

After, we need to update `User` Model, and add proper lazy select for field

``` python
--8<-- "docs/snippets/sqlalchemy_models.py:oauth-user"
```

## Repositories
To make the library as extensible as possible, we chose the Service-Repository architecture.
So we need to implement repository class for every ORM Model.

``` python
--8<-- "docs/snippets/sqlalchemy_repos.py:repos"
```

Inside this classes we can override methods to get items from DB.
After creation repos, we need to create dependencies, by using FastAPI Depends function, this is very simple.

``` python
--8<-- "docs/snippets/sqlalchemy_repos.py:deps"
```

!!!tip "SessionDep"
    `SessionDep` is just annotation for sqlalchemy async session generator
    ``` python
    from typing import Annotated
    from fastapi import Depends
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

    engine = create_async_engine("<DATABASE_URL>", echo=True)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)


    async def get_session():
        async with session_factory() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()


    SessionDep = Annotated[AsyncSession, Depends(get_session)]

    ```

## Token Storage
For user authentication, we need to use tokens. Tokens should be stored somewhere or have a mechanism for verifying authenticity.
For this features we use `BaseTokenStorage` class, which handle how and where store tokens. The most simple token storage is jwt, because we do not need to use DB
or Redis to store it physicaly. To work with JWT we need to make dependencies with `JWTTokenStorage` class

``` python
from fastauth.storage import JWTTokenStorage

def get_auth_storage():
    return JWTTokenStorage(settings)

```

## Services

After creating repositories and token storage, we need to implement AuthService class, which handle all business login such as login, token creation, etc.
Inside class we can override some events, such as `on_after_register`, `on_after_delete`, etc.

``` python
--8<-- "docs/snippets/sqlalchemy_service.py"
```


## Transport

We need choose throught which transport we get tokens from user in request, it can be Bearer in header or cookie token. To handle this we use `BaseTransport` class.
For example we will use `CookieTransport` which handle token recieve throught cookies.

``` python
from fastauth.transport import CookieTransport

transport = CookieTransport(settings)

```

## FastAuth

Last class which Facade for everything is `FastAuth` class. It checks the validity of tokens and whether the user has access to the resource.

``` python
from fastauth import FastAuth

security = FastAuth(settings, get_auth_service, transport)

```

## Full SQLAlchemy Example

=== "config.py"
    ``` python
    from fastauth.settings import FastAuthSettings
    from pydantic_settings import BaseSettingsModel

    class Settings(FastAuthSettings, BaseSettingsModel):
        DATABASE_URL: str = "DATABASE_URL"
        
    settings = Settings()
    ```
=== "models.py"
    ``` python
    --8<-- "docs/snippets/sqlalchemy_models.py:rbac"
    --8<-- "docs/snippets/sqlalchemy_models.py:oauth"
    --8<-- "docs/snippets/sqlalchemy_models.py:oauth-user"
    ```

=== "db.py"
    ``` python
    from .config import settings
    from typing import Annotated
    from fastapi import Depends
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)


    async def get_session():
        async with session_factory() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()


    SessionDep = Annotated[AsyncSession, Depends(get_session)]
    ```

=== "repositories.py"
    ``` python
    from .db import SessionDep
    from .models import User, Role, Permission, OAuthAccount
    --8<-- "docs/snippets/sqlalchemy_repos.py"
    ```
=== "services.py"
    ``` python
    from .config import settings
    from .repositories import UserRepoDep, OAuthRepoDep, RoleRepoDep
    from fastauth.storage import JWTTokenStorage

    def get_auth_storage():
        return JWTTokenStorage(settings)

    --8<-- "docs/snippets/sqlalchemy_service.py"
    ```
=== "security.py"
    ``` python
    from .config import settings
    from .services import get_auth_service
    from fastauth.transport import CookieTransport

    transport = CookieTransport(settings)
    security = FastAuth(settings, get_auth_service, transport)
    ```