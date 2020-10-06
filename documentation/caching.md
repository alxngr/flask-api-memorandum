# Caching

Still in the spirit of improving the performance of our API, we can use **caching**. **Caching** is the process of storing data in memory. For example, if we consider that our users are going to access their friends list a lot, instead of querying our database every time, we store the list in the server memory. Web browsers cache the recently visited websites (the most network heavy resources like images) in the local memeory of the client in order the reload those websites faster.

For server-side caching, the cache can be stored in the same server on which the application is running. Note that the cache can also be stored on a dedicated server like [Redis](https://redis.io/) or [Memcached](https://www.memcached.org/). In our case, we will store the cache on the same server as a global dictionnary (simple cache).

[Flask-Caching](https://pythonhosted.org/Flask-Caching/) allows us to easily implement a cache functionality. The cache is a dictionary where keys are used to specify the resources to cache and the values are the actual data to be stored.

First we create our cache object:

```python
from flask_caching import Cache

cache = Cache()
```

Then, we register our cache to our app:

```python
cache.init_app(app)
```

We also set some caching parameters in our configuration class:

```python
CACHE_TYPE = 'simple'
CACHE_DEFAULT_TIMEOUT = 600
```

We use a **SimpleCache** strategy and the cache is set to expire after 600s.

We can then just add a decorator to the resources we want to be cached:

```python
@cache.cached(timeout=60, query_string=True)
```

This specific resource will be cached for 60s and we allow the passing in of arguments in this example.

We also need to clear the cache when the data is updated (if not the old data will be sent back to the client). In our example, if we cache the route to get a user, we want to clear the cache once the user updates its avatar image.

We can create a simple method to clear the cache:

```python
def clear_cache(key_prefix: str) -> None:
    keys = [key for key in cache.cache._cache.keys() if key.startswith(key_prefix)]
    cache.delete_many(*keys)
```

And then clear the cache when the user avatar is changed:

```python
clear_cache('/users/{}'.format(user.username))
```
