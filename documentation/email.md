# Email Confirmation

When a user sign in on our application, we might want to ensure that the email address they provide is valid and belongs to them. Hence, we mark every new user **is_active** as **False**, send a mail to the email they provided and mark the **is_active** field as **True** when they click on a link in the activation mail. We can also limit the features available to a user that is not active.

## The [Mailgun](https://www.mailgun.com/) API

In order to send an activation mail to our new users, we use a thid-party [SMTP](https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol) (Simple Mail Transfer Protocol) that provides an API to send emails.

After registering on Mailgun, keep a note of your `domain` url and your `api key`.

We can send an email using the following class:

```python
import requests

class MailgunApi:

    API_URL = 'https://api.mailgun.net/v3/{}/messages'

    def __init__(self, domain: str, api_key: str):
        self.domain = domain
        self.key = api_key
        self.base_url = self.API_URL.format(self.domain)

    def send_email(self, to: str, subject: str, text: str, html: str=None):
        data = {
            'from': 'Our API <no-reply@{}>'.format(self.domain),
            'to': to,
            'subject': subject,
            'text': text,
            'html': html
        }

        return requests.post(url=self.base_url, auth=('api', self.key), data=data)
```

## User Account Activation

When a user registers on our application, we send an email using the Mailgun API. In this email, we include a unique link created with the [itsdangerous](https://itsdangerous.palletsprojects.com/en/1.1.x/) package. This package ensures that no one tempered with the activation email before the user followed the activation link.

In order to generate a unique token, we can follow this procedure:

```python
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def generate_token(email: str, salt: str=None) -> URLSafeTimedSerializer:
    serializer = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY'))
    return serializer.dumps(email, salt=salt)
```

And to verify a token, we can use the following method:

```python
def verify_token(token: str, max_age: int=180, salt: str=None) -> str:
    serializer = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY'))

    try:
        email = serializer.loads(token, max_age=max_age, salt=salt)
    except:
        return False

    return email
```

We can now modify **UserListResource.post**:

```python
mailgun = MailgunApi(domain='your-domain', api_key='your-api-key')

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

    token = generate_token(user.email, salt='activate')
    subject = 'Please confirm your registration.'
    link = url_for('useractivateresource', token=token, _external=True)
    text = 'Please confirm your registration by clicking on: {}'.format(link)

    mailgun.send_email(to=user.email, subject=subject, text=text)

    return user_schema.dump(user), HTTPStatus.CREATED
```

We now need to create a new resource: **UserActivateResource**. The link provided in the activation email will reach this new endpoint:

```python
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
```

And we register this new endpoint:

```python
api.add_resource(UserActivateResource, '/users/activate/<string:token>')
```

## HTML Format Email

Instead of sending a plaintext email to our users, we could send an HTML format email so that our emails are prettier. We just need to pass the HTML code as a parameter to the **mailgun.send_email** method:

```python
mailgun.send_email(to=user.email, subject=subject, text=text, html='<html><body><h1>Title</h1></body></html>')
```

This would obviously be a bit of a hassle if our HTML code was longer. Flask provides a **render_template()** method that uses the [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) template engine. We can just place our HTML code under a `/templates`folder in the application project and then pass the template to the Flask **render_template** method to generate the HTML code:

```python
mailgun.send_email(to=user.email, subject=subject, text=text, html=render_template(email.html))
```

Moreover, a template handles variables that can be set by the **render_template** method. For example, our HTML and Python code can become:

```html
<html><body><h1>{{title}}</h1></body></html>
```

```python
mailgun.send_email(to=user.email, subject=subject, text=text, html=render_template(email.html, title='Title'))
```
