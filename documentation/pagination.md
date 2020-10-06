# Pagination, Searching and Ordering

When using our API, we could have an endpoint to get all the friends of an user: `/users/<string:username>/friends`. While this would work on a simple development environment, it would rapidly clutter our server if a user had a lot of friends.

**Pagination** is a way to solve this problem. When an user request its friends list, we only provide a subset of it with a link to get the previous and the next subsets. Effectively, we have split the list into pages and each page contains a link to the previous and the next pages. It is important to notice that the way we order the list is going to have a great impact on the user experience (last friends added, most common friends, most popular friends and so on...).

**Flask-SQLAlchemy** provides a convenient method to implement a **paginated API**. Here is the kind of response we would expect from it:

```json
{
    "links": {
        "first": "http://127.0.0.1:5000/users/dummy/friends?per_page=2&page=1",
        "last": "http://127.0.0.1:5000/users/dummy/friends?per_page=2&page=5",
        "prev": "http://127.0.0.1:5000/users/dummy/friends?per_page=2&page=1",
        "next": "http://127.0.0.1:5000/users/dummy/friends?per_page=2&page=3"
    },
    "page": 2,
    "pages": 5,
    "per_page": 2,
    "total": 9,
    "data": [
        {
            "username": "friends1"
        },
        {
            "username": "friends2"
        }
    ]
}
```

## The Pagination Schema

In order to have a paginated API, we first need to create a marshmallow pagination schema:

```python
class PaginationSchema(Schema):
    class Meta:
        ordered = True

    links = fields.Method(serialize='get_pagination_links')
    page = fields.Integer(dump_only=True)
    pages = fields.Integer(dump_only=True)
    per_page = fields.Integer(dump_only=True)
    total = fields.Integer(dump_only=True)

    @staticmethod
    def get_url(page: int) -> str:
        query_args = request.args.to_dict()
        query_args['page'] = page
        return '{}?{}'.format(request.base_url, urlencode(query_args))

    def get_pagination_links(self, paginated_objects) -> dict:
        pagination_links = {
            'first': self.get_url(page=1),
            'last': self.get_url(page=paginated_objects.pages)
        }

        if paginated_objects.has_prev:
            pagination_links['prev'] = self.get_url(page=paginated_objects.prev_num)

        if paginated_objects.has_next:
            pagination_links['next'] = self.get_url(page=paginated_objects.next_num)

        return pagination_links
```

## A Paginated Endpoint

Let's create a paginated endpoint at `/users/<string:username>/friends` so that a user can retrieve its friends list. We decide to paginate this endpoint because a user could have many friends and we want to avoid any clutter on our server. Hence, we first define a schema that inherits from the **PaginationSchema**:

```python
class UserPaginationSchema(PaginationSchema):
    data = fields.Nested(UserSchema, attribute='items', many=True)
```

Now, we need to add a method to our user model in order to get all of the user's friends:

```python
def get_all_friends(self, page: int, per_page: int):
    return self.friends.order_by(desc(User.created_at)).paginate(page=page, per_page=per_page)
```

Finally, we create a new resource to add our new endpoint:

```python
from webargs import fields
from webargs.flaskparser import use_kwargs

class UserFriendsResource(Resource):
    @use_kwargs({'page': fields.Int(missing=1), 'per_page': fields.Int(missing=20)}, location='query')
    @jwt_required
    def get(self, page: int, per_page: int):
        user = User.get_by_id(id=get_jwt_identity())

        if not user:
            return {'msg': 'user not found'}, HTTPStatus.NOT_FOUND

        paginated_friends = user.get_all_friends(page=page, per_page=per_page)

        return user_pagination_schema.dump(paginated_friends), HTTPStatus.OK
```

As usual, we also register this new endpoint in our app:

```python
api.add_resource(UserFriendsResource, '/users/<string:username/friends')
```

## Searching

With the pagination function, we are greatly reducing the amount of data going back to the user when it asks for its friends list. However, if the user is looking for a specific friend, it will have to scroll to many pages before finding it.

It is more convenient for the user to have the ability to search for a friend (using its username for example) and then to order the pages from the username the most likely to match our search term to the least likely. In order to do that, we will allow the client to pass a **q** parameter to search for a specific user using its username. For that purpose, we can use the **LIKE** (case-sensitive) or the **ILIKE** (case-insensitive) operators. Those operators look for an exact match which can be inconvenient for the user. To look for similar usernames, we can surround the search term with the **%** character. For example, **dummy** will look for an user with this exact username while **%dummy%** will also match with "dummy123" and so on.

We can modify the **get_all_friends** method as such:

```python
from sqlalchemy import asc, desc, or_

def get_all_friends(self, q: str, page: int, per_page: int):
    keyword = '%{keyword}%'.format(keyword=q)
        
    return self.friends.filter(or_(User.username.ilike(keyword), User.email.ilike(keyword))).order_by(desc(User.created_at)).paginate(page=page, per_page=per_page)
```

NB: Notice that we use the **or_** method from **SQLAlchemy** in order to match either with the username or the email of the user's friends.

We also modify the **UserFriendsResource** in order to pass the **q** parameter to it:

```python
class UserFriendsResource(Resource):
    @use_kwargs({'q': fields.Str(missing=''), 'page': fields.Int(missing=1), 'per_page': fields.Int(missing=20)}, location='query')
    @jwt_required
    def get(self, q: str, page: int, per_page: int):
        user = User.get_by_id(id=get_jwt_identity())

        if not user:
            return {'msg': 'user not found'}, HTTPStatus.NOT_FOUND

        paginated_friends = user.get_all_friends(q=q, page=page, per_page=per_page)

        return user_pagination_schema.dump(paginated_friends), HTTPStatus.OK
```

## Sorting and Ordering

While our user is able to search for a specific friend, it can be convenient to give it the ability to order the results (in a ascending or descending order) according to another parameter (like the date at which the user profile was last updated).

This can easily been achieved by using the **sort** and **order** parameters.

First, we modify the **get_all_friends** method:

```python
def get_all_friends(self, q: str, page: int, per_page: int, sort: str, order: str):
    keyword = '%{keyword}%'.format(keyword=q)

    if order == 'asc':
        sort_logic = asc(getattr(User, sort))
    else:
        sort_logic = desc(getattr(User, sort))
    
    return self.friends.filter(or_(User.username.ilike(keyword), User.email.ilike(keyword))).order_by(sort_logic).paginate(page=page, per_page=per_page)
```

Then, we update our **UserFriendsResource**:

```python
class UserFriendsResource(Resource):
    @use_kwargs({'q': fields.Str(missing=''), 'page': fields.Int(missing=1), 'per_page': fields.Int(missing=20), 'sort': fields.Str(missing='created_at'), 'order': fields.Str(missing='desc')}, location='query')
    @jwt_required
    def get(self, q: str, page: int, per_page: int, sort: str, order: str):
        user = User.get_by_id(id=get_jwt_identity())

        if not user:
            return {'msg': 'user not found'}, HTTPStatus.NOT_FOUND

        if not sort in ['created_at', 'updated_at']:
            sort = 'created_at'

        if not order in ['asc', 'desc']:
            order = 'desc'

        paginated_friends = user.get_all_friends(q=q, page=page, per_page=per_page, sort=sort, order=order)

        return user_pagination_schema.dump(paginated_friends), HTTPStatus.OK
```
