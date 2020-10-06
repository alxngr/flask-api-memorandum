import os
from subprocess import run
import sys
import requests

from dotenv import load_dotenv

from PIL import Image

import psycopg2

from config import DevelopmentConfig as cfg


def set_project(my_email: str):
    check_database()
    
    passed = check_environment_variables()
    if not passed:
        return

    create_static_folders()
    create_default_avatar()
    fill_db(my_email)

def check_database() -> None:
    try:
        conn = psycopg2.connect(dbname=cfg.SQLALCHEMY_DATABASE_DBNAME, user=cfg.SQLALCHEMY_DATABASE_USERNAME, password=cfg.SQLALCHEMY_DATABASE_PASSWORD)
        conn.close()
        print('Managed to connect to database.')
    except Exception as err:
        print(f'Unable to connect to database:{err}')

def check_environment_variables() -> bool:
    load_dotenv()

    if os.environ.get('ENV') != 'Development':
        print('Environemnent is not set to use Development Configuration.')
        return False

    if os.environ.get('MAILGUN_DOMAIN') == 'your-mailgun-domain':
        print('Mailgun domain is not set. Register at https://www.mailgun.com/')
        return False

    if os.environ.get('MAILGUN_API_KEY') == 'your-mailgun-api-key':
        print('Mailgun api key is not set. Register at https://www.mailgun.com/')
        return False

    print('Environment variables seems to be valid.')
    return True
    
def create_static_folders() -> None:
    static = cfg.ROOT / 'static'
    static.mkdir(exist_ok=True)

    images = static / 'images'
    images.mkdir(exist_ok=True)
    
    assets = images / 'assets'
    assets.mkdir(exist_ok=True)

    avatars = images / 'avatars'
    avatars.mkdir(exist_ok=True)

    print('Created necessary folders.')

def create_default_avatar() -> None:
    img = Image.new('RGB', (512, 512), (200, 200, 200))
    filepath = cfg.ROOT / 'static' / 'images' / 'assets' / 'default-avatar.jpg'
    img.save(filepath, 'JPEG')

    print('Created default avatar image.')

def fill_db(my_email: str) -> None:
    users = [
        {
            'username': 'dummy0',
            'email': str(my_email),
            'password': '123'
        },
        {
            'username': 'dummy1',
            'email': 'dummy1@dummy.com',
            'password': '123'
        },
        {
            'username': 'dummy2',
            'email': 'dummy2@dummy.com',
            'password': '123'
        },
        {
            'username': 'dummy3',
            'email': 'dummy3@dummy.com',
            'password': '123'
        },
        {
            'username': 'dummy4',
            'email': 'dummy4@dummy.com',
            'password': '123'
        }
    ]

    for user in users:
        response = requests.post('http://127.0.0.1:5000/users', json=user)
        username = user['username']
        print(f'Adding {username}: {response.json()}')

    print('Filled database with some users.')


if __name__ == '__main__':
    args = sys.argv
    if len(args) <= 1:
        print('Please provide a email address in order to activate an user account with Mailgun API.')
        pass
    elif len(args) > 2:
        print('Too many arguments provided.')
    else:
        set_project(my_email=args[1])
