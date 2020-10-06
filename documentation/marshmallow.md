# Object Serialization with marshmallow

It is vital to ensure that the information passed by the client is in the format that we expect. For example, the client could pass a string for a user's id while our server requires an integer. The [marshmallow](https://marshmallow.readthedocs.io/en/stable/) package verify both the information sent by the client and by the server. By ensuring the integrity of the data, we improve the quality of our API.

The marshmallow package essentially lets us serialize/deserialize our models (python objects) by defining a schema for it.

## Defining a schema

Following our example, we can define a schema for a user:

```python
from marshmallow import Schema, fields

from utils import hash_password


class UserSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(dump_only=True)

    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.Method(required=True, deserialize='load_password')
    avatar_url = fields.Method(serialize='dump_avatar_url')
    friends = fields.Pluck('self', 'id', many=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    def load_password(self, value: str) -> str:
        return hash_password(value)
```

## Using a schema

In order to use our user schema, we start be instantiating two schemas objects: one for the logged user and the other non-logged user. When a user is not logged, it cannot access the email and friends fields:

```python
user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email', 'friends',))
```

Then the **UserListResource.post** method becomes:

```python
def post(self):
    json_data = request.get_json()

    try:
        data = user_schema.load(data=json_data)
    except ValidationError as err:
        return {'msg': 'validation errors', 'errors': err}, HTTPStatus.BAD_REQUEST

    if User.get_by_username(username=data.get('username')):
        return {'msg': 'username already used'}, HTTPStatus.BAD_REQUEST

    if User.get_by_email(email=data.get('email')):
        return {'msg': 'email already used'}, HTTPStatus.BAD_REQUEST

    user = User(**data)
    user.save()

    return user_schema.dump(user), HTTPStatus.CREATED
```
