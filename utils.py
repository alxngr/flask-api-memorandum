import os
import sys

import uuid

from passlib.hash import pbkdf2_sha256

from itsdangerous import URLSafeTimedSerializer

from flask import current_app
from flask_uploads import extension

from PIL import Image

import logging
from logging.handlers import TimedRotatingFileHandler

from config import Config

from extensions import image_set, cache


def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)

def check_password(password: str, hashed: str) -> bool:
    return pbkdf2_sha256.verify(password, hashed)

def generate_token(email: str, salt: str=None) -> URLSafeTimedSerializer:
    serializer = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY'))
    return serializer.dumps(email, salt=salt)

def verify_token(token: str, max_age: int=180, salt: str=None) -> str:
    serializer = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY'))

    try:
        email = serializer.loads(token, max_age=max_age, salt=salt)
    except:
        return False
    
    return email

def save_image(image, folder: str) -> str:
    filename = '{}.{}'.format(uuid.uuid4(), extension(image.filename))
    image_set.save(image, folder=folder, name=filename)

    filename = compress_image(filename=filename, folder=folder)

    return filename

def compress_image(filename: str, folder: str) -> str:
    file_path = image_set.path(filename=filename, folder=folder)

    image = Image.open(file_path)

    if image.mode != "RGB":
        image = image.convert("RGB")

    if max(image.width, image.height) > 1600:
        maxsize = (1600, 1600)
        image.thumbnail(maxsize)

    compressed_filename = '{}.jpg'.format(uuid.uuid4())
    compressed_file_path = image_set.path(filename=compressed_filename, folder=folder)

    image.save(compressed_file_path, optimize=True, quality=85)

    os.remove(file_path)

    return compressed_filename

def clear_cache(key_prefix: str) -> None:
    keys = [key for key in cache.cache._cache.keys() if key.startswith(key_prefix)]
    cache.delete_many(*keys)

def get_console_handler() -> logging.Handler:
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(Config.FORMATTER)
    return console_handler

def get_file_hanlder() -> logging.Handler:
    file_handler = TimedRotatingFileHandler(Config.LOG_FILE, when='midnight')
    file_handler.setFormatter(Config.FORMATTER)
    file_handler.setLevel(logging.WARNING)
    return file_handler

def get_logger(logger_name: str) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    
    logger.setLevel(logging.INFO)

    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_hanlder())
    logger.propagate = False

    return logger
