# Flask-RESTful

[Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/) is a Flask extension that allows for quick API development when compared to the built-in wrapper **@app.route('/')**. It allows us to maintain and structure the API endpoints in a better and easier way.

## Creating a Model

In order to structure our API, we can define a model for a user as such:

```python
class User:
    def __init__(self, username: str, password: str):
        self.id: int = get_last_id()
        self.username: str = username
        self.password: str = password

    @property
    def data(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }
```

We also define a "data" property to easily get a dictionary representing our user.

## Resourceful Routing

The main building blocks in Flask-RESTful are resources. The idea behind them is that we want to structure all the client's requests around resources. In our example, we are going to group all the CRUD actions on a user under **UserResource**. This provides a clear structure to follow.

In order to implement **UserResource**, we simply inherit from the **flask_restful.Resource** class and implement methods that correspond to the HTTP verb inside it.

Here we create two resources: **UserListResource** and **UserResource**. One to access all users and the other to access a specific user.

```python
class UserListResource(Resource):
    def get(self):
        data = [user.data for user in users]

        return {'data': data}, HTTPStatus.OK

    def post(self):
        data = request.get_json()
        user = User(username=data['username'], password=data['password'])
        users.append(user)

        return user.data, HTTPStatus.CREATED

class UserResource(Resource):
    def get(self, id: int):
        user: User = next((user for user in users if user.id == id), None)

        if not user:
            return {'msg': 'user not found'}, HTTPStatus.NOT_FOUND

        return user.data, HTTPStatus.OK

    def put(self, id: int):
        data = request.get_json()
        user: User = next((user for user in users if user.id == id), None)

        if not user:
            return {'msg': 'user not found'}, HTTPStatus.NOT_FOUND

        user.username = data['username']
        user.password = data['password']

        return user.data, HTTPStatus.OK

    def delete(self, id: int):
        user: User = next((user for user in users if user.id == id), None)

        if not user:
            return {'msg': 'user not found'}, HTTPStatus.NOT_FOUND

        users.remove(user)

        return {}, HTTPStatus.NO_CONTENT
```

NB: Each endpoint does not need to jsonify the returned data as **Flask-RESTful** does it for us.

## Configuring Endpoints

Once we have defined our resources, we set up the endpoints so that a client can request them. We use the **add_resource** method on the API object to specify the URL for these endpoints and route the client HTTP requests to our resources.

```python
from flask import Flask
from flask_restful import Api

from resources.user import UserListResource, UserResource

app = Flask(__name__)
api = Api(app)

api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:id>')

if __name__ == '__main__':
    app.run()
```
