import os

from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Api
from flask_uploads import configure_uploads, patch_request_class

from dotenv import load_dotenv

from extensions import db, jwt, image_set, cache, limiter

from resources.user import (
    UserListResource, 
    UserResource, 
    MeResource, 
    UserActivateResource, 
    UserAvatarUploadResource, 
    UserFriendsListResource,
    UserFriendsResource
)
from resources.token import TokenResource, RefreshToken, RevokeResource, blacklist

from utils import get_logger


def create_app() -> Flask:
    # Environment variables
    load_dotenv()

    # Configuration type
    env = os.environ.get('ENV', 'Development')

    if env == 'Production':
        conf_str = 'config.ProductionConfig'
    elif env == 'Staging':
        conf_str = 'config.StagingConfig'
    else:
        conf_str = 'config.DevelopmentConfig'

    # Create logger
    logger = get_logger(logger_name=__name__)
    
    # Create Flask app, set configuration and register extensions
    app = Flask(__name__)
    app.config.from_object(conf_str)
    
    register_extensions(app)
    register_resources(app)

    logger.debug('Application instance created')
    
    return app

def register_extensions(app: Flask) -> None:
    db.init_app(app)
    Migrate(app, db)
    jwt.init_app(app)
    configure_uploads(app, image_set)
    patch_request_class(app, 10 * 1024 * 1024)
    cache.init_app(app)
    limiter.init_app(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token: dict) -> bool:
        jti = decrypted_token['jti']
        return jti in blacklist
    
def register_resources(app: Flask) -> None:
    api = Api(app)

    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<string:username>')
    api.add_resource(MeResource, '/me')
    api.add_resource(UserActivateResource, '/users/activate/<string:token>')
    api.add_resource(UserAvatarUploadResource, '/users/avatar')
    api.add_resource(UserFriendsListResource, '/users/friends')
    api.add_resource(UserFriendsResource, '/users/friends/<string:username>')
    
    api.add_resource(TokenResource, '/token')
    api.add_resource(RefreshToken, '/refresh')
    api.add_resource(RevokeResource, '/revoke')

@limiter.request_filter
def ip_whitelist():
    return request.remote_addr == '127.0.0.1'


if __name__ == '__main__':
    app = create_app()
    app.run()
