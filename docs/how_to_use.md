# How use

For creating protected route, we just need call dependency for `FastAuth` class

``` python

from fastapi import FastAPI, Depends
from .security import security
from fastauth.schemas.auth import TokenData


app = FastAPI()

@app.get('/unprotected')
async def unprotected_route():
    return {"hello":"world"}

# First we check if set token, and if it`s valid, then we fetch TokenData and return it.

@app.get('/protected')
async def protected_route(token: TokenData = Depends(security.get_access_token())):
    return token

```

For use protection by permission we call `security.require_permission`

``` python

# First we check if token set, then we check if user has access to do action in resource, then return TokenData
@app.get('/protected')
async def protected_route(token: TokenData = Depends(security.require_permission("resource:read"))):
    return token

```

!!!tip "Permission string"
    To verify permission we need pass correct string in format:`RESOURCE:ACTION`
    Where resource and action stored in DB in acording fields
    
## Features

`FastAuth` class have some methods for protection:

- `get_access_token()`: Check if token set and have 'ACCESS' Type
- `get_refresh_token()`: Check if token set and have 'REFRESH' Type
- `get_current_user()`: Check if token is access and fetch current user from DB
- `require_permission(permission:str)`: Check if user in token have provided permission
- `require_rolr(role:str)`: Check if user in token have provided role
- `require_any_permission(permissions: list[str])`: Check if user have at least one permission from provided
- `require_all_permissions(permissions: list[str])`: Check if user have all permission from provided
- `get_login_response(tokens: TokenResponse)`: Convert dataclass with tokens to FastAPI Response acording to Transport(Cookie Response, JSONResponse)
- `get_logout_response()`: Return logout response