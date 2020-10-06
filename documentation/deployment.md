# Deployment

In order to prepare for a future deployment of our application, we need to change mainly two things:

* Have separate configurations for development, staging (simulating a production environment on our local machine) and production.

* Handle our environment variables differently, using python-dotenv on our local machine and setting them on the production server.

Hence, we create three classes for our configuration inheriting the Configuration class:

```python
class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{your_name}:{your_password}@localhost/{db_name}'

    SECRET_KEY = 'secret-key'


class StagingConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
```

In our app, we then handle the different scenarios:

```python
def create_app() -> Flask:
    load_dotenv()

    env = os.environ.get('ENV', 'Development')

    if env == 'Production':
        conf_str = 'config.ProductionConfig'
    elif env == 'Staging':
        conf_str = 'config.StagingConfig'
    else:
        conf_str = 'config.DevelopmentConfig'

    app = Flask(__name__)
    app.config.from_object(conf_str)
    register_extensions(app)
    return app
```

NB: We use [python-dotenv](https://github.com/theskumar/python-dotenv) to load our environment variables stored in `.env` file.

NB: Depending on where we deploy our app (Heroku, AWS, Azure...), we might need to set our environment variables differently.
