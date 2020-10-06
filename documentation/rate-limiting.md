# API Rate Limiting

We can further improve the performance of our API by limiting how much a user (identified by its IP address) can query it. The idea is to share the resources of our server between our users and to not have a small amount of "intensive" users using all the resources. In order to do this, we limit the number of requests per user (like 10 per second) and all requests in excess will just be ignored by the server.

We can use HTTP headers to display the rate limit to the client:

* **X-RateLimit-Limit**: the rate limit of the endpoint.

* **X-RateLimit-Remaining**: the number of remaining requests.

* **X-RateLimit-Reset**: the time when the next reset will occur (UTC).

* **Retry-After**: the number of seconds before the next reset.

If a client exceeds its requests count, it will receive a **429 Too Many Requests** status code.

[Flask-Limiter](https://flask-limiter.readthedocs.io/en/stable/) lets us easily implement such a functionality. It can add the rate-limiting feature to an endpoint but also put the rate limiting information in the HTTP header.

It uses the following syntax:

```txt
[count] [per|/] [n (optional)] [second|minute|hour|day|month|year]
```

For example, `10 per minute`is a valid syntax.

We first create a limiter object:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
```

The **get_remote_address** function will return the IP address of the current request.

Then, we register our limiter with our app:

```python
limiter.init_app(app)
```

We also set our configuration variables in order to pass the rate limiting information to the HTTP header:

```python
RATELIMIT_HEADERS_ENABLED = True
```

Finally, we add the following line to any of our resources to limit it:

```python
decorators = [limiter.limit('10 per minute', methods=['GET'], error_message='Too Many Requests')]
```

NB: We can add a whitelist that will not be subject to the limiter (for developers or special users) by adding the following method to our app:

```python
@limiter.request_filter
def ip_whitelist():
    return request.remote_addr == '127.0.0.1'
```
