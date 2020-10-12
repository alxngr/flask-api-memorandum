# Appendix

## Cloning the project and Setting up the virtual environment

1. Clone this repository

```zsh
git clone <repo-url>
cd <repo-name>
```

2. Create a virtual environment (assuming venv is installed on your machine)

```zsh
python -m venv venv/
```

3. Install requirements

```zsh
source venv/bin/activate
pip install -r requirements.txt
```

4. Launch the server

```zsh
python app.py
```

## Creating our local database using PgAdmin

In order to create a local Postgres database on our machine, we use [PgAdmin](https://www.pgadmin.org/). Once it is installed along with Postgres, follow these simple steps:

1. Create a role. *Right-click* on **PostgreSQL12** under **Servers**, select **Create** and then **Login/Group Role...**.

2. Fill in the login name (keep track of it). In the **Definition** tab, create a password (keep track of it too).

3. In the **Privileges**, and select **Yes** for **Can login?**.

4. *Right-click* on **Databases**, and create a database.

5. Name your database, and set the role you have just created to **Owner**. Save.

6. Set the `SQLALCHEMY_DATABASE_DBNAME`, `SQLALCHEMY_DATABASE_USERNAME` and `SQLALCHEMY_DATABASE_PASSWORD` variables in the **DevelopmentConfig** class located in `config.py`.

## Mailgun

In order to send an activation email to our new users, we use the Mailgun API:

1. Register on [Mailgun](https://www.mailgun.com/).

2. Retrieve your domain name and api key.

3. Set your the `MAILGUN_DOMAIN` and `MAILGUN_API_KEY` in the `.env` file.

## Create a Secret Key

You will also need to generate a secret key. It should be as random as possible. You can run the following code to create one:

```python
from secrets import token_hex

print(token_hex(16))
```

You can set it in `config.py`.

## Quick Setup

Finally, you can run the `quick_setup.py` script by running the following commands in the terminal (from the project folder):

```bash
source venv/bin/activate
python quick_setup.py "your-email"
```

The script performs the following operations:

1. Check the ability to connect to your database.

2. Check that you have set the environment variables in the `.env` file.

3. Create the necessary folders to store users avatar images.

4. Create a default avatar image.

5. Fill the database with some users. The first user will have your mail address so that you can check that the Mailgun API is working. You can activate this account by following the link sent to your mail address (the activation mail might be in your spam folder).

## Postman

If you want to use [Postman](https://www.postman.com/) to test the API endpoints, you can load the Postman collection located at `/postman/Users API.postman_collection.json`.
