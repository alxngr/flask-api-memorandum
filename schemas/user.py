from flask import url_for
from marshmallow import Schema, fields

from models.user import User
from schemas.pagination import PaginationSchema

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

    def dump_avatar_url(self, user: User):
        if user.avatar_image:
            return url_for('static', filename='images/avatars/{}'.format(user.avatar_image), _external=True)
        else:
            return url_for('static', filename='images/assets/default-avatar.jpg', _external=True)


class UserPublicSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(dump_only=True)

    username = fields.String(required=True)
    avatar_url = fields.Method(serialize='dump_avatar_url')

    def dump_avatar_url(self, user: User):
        if user.avatar_image:
            return url_for('static', filename='images/avatars/{}'.format(user.avatar_image), _external=True)
        else:
            return url_for('static', filename='images/assets/default-avatar.jpg', _external=True)


class UserPaginationSchema(PaginationSchema):
    data = fields.Nested(UserSchema, attribute='items', many=True)
    

class UserPublicPaginationSchema(PaginationSchema):
    data = fields.Nested(UserPublicSchema, attribute='items', many=True)
