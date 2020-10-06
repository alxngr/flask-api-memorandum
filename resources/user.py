import os

from flask import request, url_for, render_template
from flask_restful import Resource
from flask_jwt_extended import jwt_required, jwt_optional, get_jwt_identity

from http import HTTPStatus

from marshmallow import ValidationError

from webargs import fields
from webargs.flaskparser import use_kwargs

from models.user import User
from schemas.user import UserSchema, UserPaginationSchema, UserPublicPaginationSchema

from mailgun import MailgunApi

from extensions import image_set, cache, limiter

from utils import generate_token, verify_token, save_image, clear_cache


user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email', 'friends',))
user_avatar_schema = UserSchema(only=('avatar_url',))
user_pagination_schema = UserPaginationSchema()
user_public_pagination_schema = UserPublicPaginationSchema()

mailgun = MailgunApi(domain=os.environ.get('MAILGUN_DOMAIN'), api_key=os.environ.get('MAILGUN_API_KEY'))


class UserListResource(Resource):
    decorators = [limiter.limit('5 per minute', methods=['GET'], error_message='Too Many Requests')]

    @jwt_required
    @use_kwargs({'q': fields.Str(missing=''), 
                 'page': fields.Int(missing=1), 
                 'per_page': fields.Int(missing=10), 
                 'sort': fields.Str(missing='created_at'), 
                 'order': fields.Str(missing='desc')}, location='query')
    @cache.cached(timeout=60, query_string=True)
    def get(self, q: str, page: int, per_page: int, sort: str, order: str):
        user = User.get_by_id(get_jwt_identity())
        
        if not user:
            return {'msg': 'user not found'}, HTTPStatus.NOT_FOUND

        if not sort in ['created_at', 'updated_at']:
            sort = 'created_at'
        
        if not order in ['asc', 'desc']:
            order = 'desc'
        
        users = User.get_all(q, page, per_page, sort, order)

        return user_public_pagination_schema.dump(users), HTTPStatus.OK

    def post(self):
        json_data = request.get_json()

        try:
            data = user_schema.load(data=json_data)
        except ValidationError as err:
            return {'msg': 'validation errors', 'errors': str(err)}, HTTPStatus.BAD_REQUEST
                
        if User.get_by_username(username=data.get('username')):
            return {'msg': 'username already used'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(email=data.get('email')):
            return {'msg': 'email already used'}, HTTPStatus.BAD_REQUEST
        
        user = User(**data)
        user.save()

        token = generate_token(user.email, salt='activate')
        subject = 'Please confirm your registration.'
        link = url_for('useractivateresource', token=token, _external=True)
        text = 'Please confirm your registration by clicking on: {}'.format(link)

        mailgun.send_email(to=user.email, subject=subject, text=text, html=render_template('email/activation.html', link=link))

        clear_cache('/users/')

        return user_schema.dump(user), HTTPStatus.CREATED


class UserResource(Resource):
    @jwt_optional
    def get(self, username: str):
        user = User.get_by_username(username=username)

        if not user:
            return {'msg': 'user not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()

        if current_user == user.id:
            data = user_schema.dump(user)
        else:
            data = user_public_schema.dump(user)

        return data, HTTPStatus.OK

    @jwt_required
    def patch(self, username: str):
        json_data = request.get_json()
        user = User.get_by_id(id=get_jwt_identity())

        if not user:
            return {'msg': 'user not found'}, HTTPStatus.NOT_FOUND
        
        user.username = json_data.get('username') or user.username
        user.email = json_data.get('email') or user.email
        user.password = json_data.get('password') or user.password

        user.save()

        return user_schema.dump(user), HTTPStatus.OK

    @jwt_required
    def delete(self, username: str):
        user = User.get_by_id(id=get_jwt_identity())

        if not user:
            return {'msg': 'user not found'}, HTTPStatus.NOT_FOUND
        
        user.delete()
        
        return {}, HTTPStatus.NO_CONTENT


class MeResource(Resource):
    @jwt_required
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())

        if not user:
            return {'msg': 'user not found'}, HTTPStatus.NOT_FOUND
        
        return user_schema.dump(user), HTTPStatus.OK


class UserActivateResource(Resource):
    def get(self, token: str):
        email = verify_token(token, salt='activate')

        if email is False:
            return {'msg': 'invalid token or token expired'}, HTTPStatus.BAD_REQUEST

        user = User.get_by_email(email=email)

        if not user:
            return {'msg': 'user not found'}, HTTPStatus.NOT_FOUND

        if user.is_active:
            return {'msg': 'user account is already activated'}, HTTPStatus.BAD_REQUEST

        user.is_active = True
        user.save()        

        return {}, HTTPStatus.NO_CONTENT


class UserAvatarUploadResource(Resource):
    @jwt_required
    def put(self):
        file = request.files.get('avatar')

        if not file:
            return {'msg': 'not a valid image'}, HTTPStatus.BAD_REQUEST
        
        if not image_set.file_allowed(file, file.filename):
            return {'msg': 'file type not allowed'}, HTTPStatus.BAD_REQUEST
        
        user = User.get_by_id(id=get_jwt_identity())

        if not user:
            return {'msg': 'user not found'}, HTTPStatus.NOT_FOUND

        if user.avatar_image:
            avatar_path = image_set.path(folder='avatars', filename=user.avatar_image)
            if os.path.exists(avatar_path):
                os.remove(avatar_path)

        filename = save_image(image=file, folder='avatars')

        user.avatar_image = filename
        user.save()

        clear_cache('/users/{}'.format(user.username))

        return user_avatar_schema.dump(user), HTTPStatus.OK


class UserFriendsListResource(Resource):
    decorators = [limiter.limit('10 per minute', methods=['GET'], error_message='Too Many Requests')]

    @jwt_required
    @use_kwargs({'q': fields.Str(missing=''), 
                 'page': fields.Int(missing=1), 
                 'per_page': fields.Int(missing=20), 
                 'sort': fields.Str(missing='created_at'), 
                 'order': fields.Str(missing='desc')}, location='query')
    @cache.cached(timeout=60, query_string=True)
    def get(self, q: str, page: int, per_page: int, sort: str, order: str):
        user = User.get_by_id(id=get_jwt_identity())
        
        if not user:
            return {'msg': 'user not found'}, HTTPStatus.NOT_FOUND
        
        if not sort in ['created_at', 'updated_at']:
            sort = 'created_at'
        
        if not order in ['asc', 'desc']:
            order = 'desc'

        paginated_friends = user.get_all_friends(q=q, page=page, per_page=per_page, sort=sort, order=order)
        
        return user_pagination_schema.dump(paginated_friends), HTTPStatus.OK


class UserFriendsResource(Resource):
    @jwt_required
    def patch(self, username: str):
        user = User.get_by_id(get_jwt_identity())

        if not user:
            return {'msg': 'user not found'}, HTTPStatus.NOT_FOUND
        
        friend = User.get_by_username(username=username)

        if not friend:
            return {'msg': 'friend not found'}, HTTPStatus.NOT_FOUND
        
        if user.id == friend.id:
            return {'msg': 'user cannot be friend with itself'}, HTTPStatus.BAD_REQUEST
                
        if any(friend.id==f.id for f in user.friends):
            return {'msg': 'user is already friend with other user'}, HTTPStatus.BAD_REQUEST
        
        user.friends.append(friend)
        friend.friends.append(user)
        
        user.save()
        friend.save()
        
        return user_schema.dump(user), HTTPStatus.OK

    @jwt_required
    def delete(self, username: str):
        user = User.get_by_id(get_jwt_identity())

        if not user:
            return {'msg': 'user not found'}, HTTPStatus.NOT_FOUND
        
        friend = User.get_by_username(username=username)

        if not friend:
            return {'msg': 'friend not found'}, HTTPStatus.NOT_FOUND
        
        if not any(friend.id==f.id for f in user.friends):
            return {'msg': 'user is not friend with other user'}, HTTPStatus.BAD_REQUEST
        
        user.friends.remove(friend)
        friend.friends.remove(user)
        
        user.save()
        friend.save()

        return user_schema.dump(user), HTTPStatus.OK
