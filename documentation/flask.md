# The Flask Web Framework

## A simple usage

[Flask](https://flask.palletsprojects.com/en/1.1.x/) is a [Python](https://en.wikipedia.org/wiki/Python_%28programming_language%29) web framework. It comes with core functionalities such as interacting with client requests, routing URLs to resources, rendering web pages and interacting with server-side databases.

Here is an example of a barebone Flask application:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
```

If this application runs on the machine of the user, querying `http://127.0.0.1:5000/` will return the string "Hello World!". The decorator above the hello_world function specify the route at which the function will be called.

NB: By default, the server runs on the port 5000 of the user machine.

## A more complex example

Here is a more complex example for an application that manages users. This application defines a route to retrieve all users and a route to retrieve an user with a specific id. In this example, the user's array lives in the application memory. If we were adding users to this array, any server shutdown would erase any changes made to this array.

```python
from flask import Flask, jsonify, request

from http import HTTPStatus

app = Flask(__name__)

users = [
    {
        "id": 1,
        "username": "Anakin",
    },
    {
        "id": 2,
        "username": "Luke",
    }
]

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify({'data': users}), HTTPStatus.OK

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id: int):
    user = next((user for user in users if user['id'] == id), None)

    if user:
        return jsonify(user), HTTPStatus.OK

    return jsonify({'msg': 'user not found'}), HTTPStatus.NOT_FOUND
```

We could also define a route to create, update and delete a user as such:

```python
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')

    user = {
        "id": len(users) + 1,
        "username": username
    }

    users.append(user)

    return jsonify(user), HTTPStatus.CREATED

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id: int):
    data = request.get_json()
    username = data.get('username')

    user = next((user for user in users if user['id'] == id), None)

    if not user:
        return jsonify({'msg': 'user not found'}), HTTPStatus.NOT_FOUND

    user.update({
        "username": username
    })

    return jsonify(user), HTTPStatus.OK

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id: int):
    user = next((user for user in users if user['id'] == id), None)

    if not user:
        return jsonify({'msg': 'user not found'}), HTTPStatus.NOT_FOUND

    users.remove(user)

    return '', HTTPStatus.NO_CONTENT
```

## How to test API endpoints

There are several ways to test your API endpoints including:

* **[cURL](https://curl.haxx.se/)**: a command-line tool that can transfer data using URLs

* **[httpie](https://httpie.org/)**: another user-friendly command-line tool

* **[Postman](https://www.postman.com/)**: a GUI tool with a wide range of capabilities
