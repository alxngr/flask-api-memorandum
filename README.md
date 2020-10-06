# Flask API Development

This memorandum goes through all the necessary steps to develop a RESTful [API](https://en.wikipedia.org/wiki/API) (Application Programming Interface) using Flask.

The example API used is a simple user management system where user can create an account, activate it with their email address, upload an avatar image and add/remove friends registered on the application.

## Summary

* [RESTful API and HTTP](documentation/restful-api.md)

  * [RESTful API](documentation/restful-api.md#restful-api)

  * [HTTP Protocol](documentation/restful-api.md#http-protocol)

  * [HTTP methods and CRUD](documentation/restful-api.md#http-methods-and-crud)

  * [The JSON Format](documentation/restful-api.md#the-json-format)

* [The Flask Web Framework](documentation/flask.md)

  * [A simple usage](documentation/flask.md#a-simple-usage)

  * [A more complex example](documentation/flask.md#a-more-complex-example)

  * [How to test API endpoints](documentation/flask.md#how-to-test-api-endpoints)

* [Flask-RESTful](documentation/flask-restful.md)

  * [Creating a Model](documentation/flask-restful.md#creating-a-model)

  * [Resourceful Routing](documentation/flask-restful.md#resourceful-routing)

  * [Configuring Endpoints](documentation/flask-restful.md#configuring-endpoints)

* [Manipulating a database with SQLAlchemy](documentation/sqlalchemy.md)

  * [Defining our Models](documentation/sqlalchemy.md#defining-our-model)

  * [Refactoring app.py](documentation/sqlalchemy.md#refactoring-app.py)

  * [Using Flask-Migrate](documentation/sqlalchemy.md#using-flask-migrate)

  * [Password Hashing](documentation/sqlalchemy.md#password-hashing)

* [Authentification Services and Security using JWT](documentation/authentification.md)

  * [Using Flask-JWT-Extended](documentation/authentification.md#using-flask-jwt-extended)

  * [The 'Me' Endpoint](documentation/authentification.md#the-'me'-endpoint)

  * [Refresh Token](documentation/authentification.md#refresh-token)

  * [User Logout](documentation/authentification.md#user-logout)

* [Object Serialization with marshmallow](documentation/marshmallow.md)

  * [Defining a schema](documentation/marshmallow.md#defining-a-schema)

  * [Using a schema](documentation/marshmallow.md#using-a-schema)

* [Email Confirmation](documentation/email.md)

  * [The Mailgun API](documentation/email.md#the-mailgun-api)

  * [User Account Activation](documentation/email.md#user-account-activation)

  * [HTML Format Email](documentation/email.md#html-format-email)

* [Using Images](documentation/images.md)

  * [User Avatar](documentation/images.md#user-avatar)

  * [Flask-Uploads](documentation/images.md#flask-uploads)

  * [Image Resizing and Compression](documentation/images.md#image-resizing-and-compression)

* [Pagination, Searching and Ordering](documentation/pagination.md)

  * [The Pagination Schema](documentation/pagination.md#the-pagination-schema)

  * [A Paginated Endpoint](documentation/pagination.md#a-paginated-endpoint)

  * [Searching](documentation/pagination.md#searching)

  * [Sorting and Ordering](documentation/pagination.md#sorting-and-ordering)

* [Caching](documentation/caching.md)

* [API Rate Limiting](documentation/rate-limiting.md)

* [Logging](documentation/logging.md)

* [Deployment](documentation/deployment.md)

* [Appendix](documentation/appendix.md)

  * [Cloning the project and Setting up the virtual environment](documentation/appendix.md#cloning-the-project-and-setting-up-the-virtual-environment)

  * [Creating our local database using PgAdmin](documentation/appendix.md#creating-our-local-database-using-pgadmin)

  * [Mailgun](documentation/appendix.md#mailgun)

  * [Create a Secret Key](documentation/appendix.md#create-a-secret-key)

  * [Quick Setup](documentation/appendix.md#quick-setup)

  * [Postman](documentation/appendix.md#postman)

* [API Reference](documentation/api-reference.md)
