# Authentification Services and Security using JWT

In order for the user to authenticate the server we use **[JWT](https://en.wikipedia.org/wiki/JSON_Web_Token)** (JSON Web Token). The token encodes the user identity and signs it digitally so that the application can control the user access based on its identity.

A **JWT** is composed of an header, a payload and a signature. The header contains the encryption type (HS512 for example). The payload content is decided by the developer, and the signature contains a public key. Only the server has the secret key that is used with the public key to decrypt the header and the signature.

Here is an example of a **JWT**:

```txt
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

The header, payload and signature are separated by a dot. Hence, the structure of a **JWT** can be resumed to **header.payload.signature**.

## Using Flask-JWT-Extended

[Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/) is a user authentification package that provides several crucial functionalities:

* **create_access_token**: a method to create a new JWT.

* **@jwt_required**: a decorator to specify which endpoints need to be protected through authentification.

* **get_jwt_identity**: a method to get the identity of a JWT.

In order, to use this package we need to add two new variables to our configuration:

```python
SECRET_KEY = 'secret-key'

JWT_ERROR_MESSAGE_KEY = 'message'
```

NB: the secret key should be random for security purposes. We will later configure environment variables and one should not publish its secret key on the web (GitHub and so on).

We can now create an instance of Flask-JWT-Extended:

```python
from flask_jwt_extended import JWTManager

jwt = JWTManager()
```

We also need to initialize the jwt object by passing our app as an argument:

```python
jwt.init_app(app)
```

Let's create a resource in order for the user to log in:

```python
from http import HTTPStatus

from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token

from utils import check_password

from models.user import User


class TokenResource(Resource):
    def post(self):
        json_data = request.get_json()

        email = json_data.get('email')
        password = json_data.get('password')

        user = User.get_by_email(email=email)

        if not user or not check_password(password=password, hashed=user.password):
            return {'msg': 'email or password is incorrect'}, HTTPStatus.UNAUTHORIZED

        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, HTTPStatus.OK
```

Now that the user has an access token, we can modify the **UserResource**. If the user is logged in, it can access all its information, if not it can only see its username:

```python
class UserResource(Resource):
    @jwt_optional
    def get(self, username: str):
        user = User.get_by_username(username=username)

        if not user:
            return {'msg': 'user not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.id:
            data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'friends': user.friends
            }
        else:
            data = {
                'id': user.id,
                'username': user.username
            }

        return data, HTTPStatus.OK
```

## The 'Me' Endpoint

It can be useful to have a resource `/users/me` for the authenticated user to get its information back using its access token.

```python
class MeResource(Resource):
    @jwt_required
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())

        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'friends': user.friends
        }

        return data, HTTPStatus.OK
```

We also need to register this new endpoint:

```python
api.add_resource(MeResource, '/me')
```

## Refresh Token

For security purpose, it is a standard practice to set an expiration date for an access token (Flask-JWT-Extended defaults it to 15 minutes). Since a token expires, we need an endpoint to refresh the token without forcing the user to put its credentials in again.

Flask-JWT-Extended provides a refresh token function. A refresh token is a token without an expiration date that can be used to generate new access tokens. However, the refresh token cannot be used to access protected endpoints.

We can also add a **fresh** attribute to our access tokens. When the user put its credentials, the **fresh** attribute is set to **True**. As soon as the user requests a new access token using a refresh token, we set the **fresh** attribute to **False**. For critical operations like changing a password, we require that the access token is fresh (hence the user might have to enter its credentials again).

Our **TokenResource** becomes:

```python
class TokenResource(Resource):
    def post(self):
        json_data = request.get_json()

        email = json_data.get('email')
        password = json_data.get('password')

        user = User.get_by_email(email=email)

        if not user or not check_password(password=password, hashed=user.password):
            return {'msg': 'email or password is incorrect'}, HTTPStatus.UNAUTHORIZED

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)
        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK
```

We also add a resource to get a new access token using a refresh token:

```python
class RefreshToken(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()

        access_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': access_token}, HTTPStatus.OK
```

We also register this new route:

```python
api.add_resource(RefreshResource, '/refresh')
```

## User Logout

In order for a user to logout, we put its token into a blacklist. Tokens in the blacklist cannot be used to access protected endpoints.

We can create a **RevokeResource** for the user to log out:

```python
blacklist = set()

class RevokeResource(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)

        return {'msg': 'Successfully logged out'}, HTTPStatus.OK
```

We also add two configurations variables to `config.py`:

```python
JWT_BLACKLIST_ENABLED = True

JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
```

After initializing the jwt object, we provide a method to check if a token is blacklisted:

```python
def register_extensions(app: Flask) -> None:
    db.init_app(app)
    Migrate(app, db)
    jwt.init_app(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token: dict) -> bool:
        jti = decrypted_token['jti']
        return jti in blacklist
```

We also register those new resources:

```python
api.add_resource(TokenResource, '/token')
api.add_resource(RefreshResource, '/refresh')
api.add_resource(RevokeResource, '/revoke')
```
