# RESTful API and HTTP

## RESTful API

[REST](https://en.wikipedia.org/wiki/Representational_state_transfer) stands for *Representational State Transfer*. It is a software architectural style that is scalable. A RESTful API refers to an API that conforms to the REST constraints/principles.

There are five important principles for the REST architecture style:

* **Client-server**: There is an interface between the client and the server. They communicate through this interface and are independant of each other. Requests always come from the client-side.

* **Stateless**: Request do not have a state. Hence, every request is considered to be independent and complete.

* **Cacheable**: Objects can be cached on the server or client side in order to improve performance.

* **Layered system**: The system can be composed of multiple layers in order to hide the logic or the resources. For example, these layers can perform different functions such as caching and encryption.

* **Uniform interface**: The interface stays the same in order to decouple the client and server logic.

## HTTP Protocol

[HTTP](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol) is an implementation of the REST architectural style. It stands for *HyperText Transfer Protocol* and is the standard protocol used on the worldwide web.

This protocol defines different types of service request methods. When the client interacts with the server API though an URL, it needs to explicitly specify the HTTP method for its request. The most common methods are:

* **GET**: read data.

* **POST**: create data.

* **PUT**: update data by completely replacing the former data.

* **PATCH**: update data by partially replacing a few attributes.

* **DELETE**: delete data.

## HTTP methods and CRUD

The vast majority of the actions performed by the API on the underlying database are [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) (*CREATE, READ, UPDATE, DELETE*). In a nutshell, CRUD models the lifecycle of the database record management.

Modeling a web application following CRUD helps easily construct a functioning web system as these actions are closely related to the HTTP protocol.

In order to pass data between the client and the server, a common communication language has to be agreed upon such as [JSON](https://en.wikipedia.org/wiki/JSON) (*JavaScript Object Notation*) or [XML](https://en.wikipedia.org/wiki/XML) (*Extensible Markup Language*).

XML has more verbose than JSON, therfore it needs more data to be passed over the network. For that very reason, JSON is usually prefered (some people also tend to consider JSON more readable by humans than XML).

## The JSON Format

The JSON format follows a few conventions:

* Names/Values exists in pairs delimited by ":"

* Objects are represented by {}

* Arrays are enclosed by []

* Strings are enclosed by ""

Here is an example of a JSON:

```json
{
    "id": 1,
    "username": "dummy",
    "password": "b5a2c96250612366ea272ffac6d9744aaf4b45aacd96aa7cfcb931ee3b558259",
    "friends": [
        {
            "id": 2,
            "username": "friends1"
        },
        {
            "id": 3,
            "username": "friends2"
        }
    ]
}
```
