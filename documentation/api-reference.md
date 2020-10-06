# API Reference

## GET **UserListResource**

```http
http://127.0.0.1:5000/users?q=search-term&page=1&per_page=3&sort=created_at&order=asc
```

*Retrieve all public users profiles.*

| **Headers** | |
| --- | --- |
| **Authorization** | Bearer "user-token-here" |


| **Params** | |
| --- | --- |
| **q** | search-term |
| **page** | 1 |
| **per_page** | 3 |
| **sort** | created_at |
| **order** | asc |

### Example Request

```bash
curl --location --request GET 'http://127.0.0.1:5000/users?q=dum&page=2&per_page=3&sort=created_at&order=asc' --header 'Authorization: Bearer <token-here>'
```

### Example Response

```json
{
    "links": {
        "first": "http://127.0.0.1:5000/users?q=dummy&page=1&per_page=3&sort=created_at&order=asc",
        "last": "http://127.0.0.1:5000/users?q=dummy&page=3&per_page=3&sort=created_at&order=asc",
        "next": "http://127.0.0.1:5000/users?q=dummy&page=2&per_page=3&sort=created_at&order=asc"
    },
    "page": 1,
    "pages": 3,
    "per_page": 3,
    "total": 7,
    "data": [
        {
            "id": 18,
            "username": "dummy0",
            "avatar_url": "http://127.0.0.1:5000/static/images/avatars/ec2d85a1-4716-4724-904d-ff79130c28d4.jpg"
        },
        {
            "id": 19,
            "username": "dummy1",
            "avatar_url": "http://127.0.0.1:5000/static/images/assets/default-avatar.jpg"
        },
        {
            "id": 20,
            "username": "dummy2",
            "avatar_url": "http://127.0.0.1:5000/static/images/assets/default-avatar.jpg"
        }
    ]
}
```

## POST **UserListResource**

```http
http://127.0.0.1:5000/users
```

*Register an user.*

### Body

```json
{
    "username": "dummy",
    "email": "dummy@gmail.com",
    "password": "dummy"
}
```

### Example Request

```bash
curl --location --request POST 'http://127.0.0.1:5000/users' \
--data-raw '{
    "username": "dummy",
    "email": "dummy@gmail.com",
    "password": "dummy123"
}'
```

### Example Response

```json
{
    "id": 1,
    "username": "dummy",
    "email": "dummy@gmail.com",
    "avatar_url": "http://127.0.0.1:5000/static/images/assets/default-avatar.jpg",
    "friends": [],
    "created_at": "1970-01-01T00:00:00.000000",
    "updated_at": "1970-01-01T00:00:00.000000"
}
```

## GET **UserResource**

```http
http://127.0.0.1:5000/users/username
```

*Get user's profile.*

| **Headers** | |
| --- | --- |
| **Authorization** | Bearer "user-token-here" |

### Example Request

```bash
curl --location --request GET 'http://127.0.0.1:5000/users/dummy' \
--header 'Authorization: Bearer <token-here>'
```

### Example Response

```json
{
    "id": 1,
    "username": "dummy",
    "email": "dummy@dummy.com",
    "avatar_url": "http://127.0.0.1:5000/static/images/avatars/ec2d85a1-4716-4724-904d-ff79130c28d4.jpg",
    "friends": [
        2,
        3,
        4
    ],
    "created_at": "1970-01-01T00:00:00.000000",
    "updated_at": "1970-01-01T00:00:00.000000"
}
```

## PATCH **UserResource**

```http
http://127.0.0.1:5000/users/username
```

*Patch a user's profile.*

| **Headers** | |
| --- | --- |
| **Authorization** | Bearer "user-token-here" |

### Example Request

```bash
curl --location --request PATCH 'http://127.0.0.1:5000/users/dummy' \
--header 'Authorization: Bearer <token-here>' \
--data-raw '{
    "email": "dummy0@dummy.com"
}'
```

### Example Response

```json
{
    "id": 1,
    "username": "dummy",
    "email": "dummy0@dummy.com",
    "avatar_url": "http://127.0.0.1:5000/static/images/avatars/ec2d85a1-4716-4724-904d-ff79130c28d4.jpg",
    "friends": [
        2,
        3,
        4
    ],
    "created_at": "1970-01-01T00:00:00.000000",
    "updated_at": "1970-01-01T00:00:00.000000"
}
```

## DELETE **UserResource**

```http
http://127.0.0.1:5000/users/username
```

*Patch a user's profile.*

| **Headers** | |
| --- | --- |
| **Authorization** | Bearer "user-token-here" |

### Example Request

```bash
curl --location --request DELETE 'http://127.0.0.1:5000/users/dummy' \
--header 'Authorization: Bearer <token-here>'
```

### Example Response

```json
{}
```

## GET **MeResource**

```http
http://127.0.0.1:5000/me
```

*Get logged user profile.*

| **Headers** | |
| --- | --- |
| **Authorization** | Bearer "user-token-here" |

### Example Request

```bash
curl --location --request GET 'http://127.0.0.1:5000/me' \
--header 'Authorization: Bearer <token-here>'
```

### Example Response

```json
{
    "id": 1,
    "username": "dummy",
    "email": "dummy@dummy.com",
    "avatar_url": "http://127.0.0.1:5000/static/images/avatars/ec2d85a1-4716-4724-904d-ff79130c28d4.jpg",
    "friends": [
        2,
        3,
        4
    ],
    "created_at": "1970-01-01T00:00:00.000000",
    "updated_at": "1970-01-01T00:00:00.000000"
}
```

## PUT **UserAvatarUploadResource**

```http
http://127.0.0.1:5000/users/avatar
```

*Update a user's avatar image.*

| **Headers** | |
| --- | --- |
| **Authorization** | Bearer "user-token-here" |

### Example Request

```bash
curl --location --request GET 'http://127.0.0.1:5000/avatar' \
--header 'Authorization: Bearer <token-here>' \
--form 'avatar=@<path-to-image>'
```

### Example Response

```json
{
    "id": 1,
    "username": "dummy",
    "email": "dummy@dummy.com",
    "avatar_url": "http://127.0.0.1:5000/static/images/avatars/ec2d85a1-4716-4724-904d-ff79130c28d4.jpg",
    "friends": [
        2,
        3,
        4
    ],
    "created_at": "1970-01-01T00:00:00.000000",
    "updated_at": "1970-01-01T00:00:00.000000"
}
```

## GET **UserFriendsListResource**

```http
http://127.0.0.1:5000/users/friends?q=search-term&page=1&per_page=3&sort=created_at&order=asc
```

*Retrieve all user"s friends profiles.*

| **Headers** | |
| --- | --- |
| **Authorization** | Bearer "user-token-here" |


| **Params** | |
| --- | --- |
| **q** | search-term |
| **page** | 1 |
| **per_page** | 3 |
| **sort** | created_at |
| **order** | asc |

### Example Request

```bash
curl --location --request GET 'http://127.0.0.1:5000/users/friends?q=dum&page=2&per_page=3&sort=created_at&order=asc' --header 'Authorization: Bearer <token-here>'
```

### Example Response

```json
{
    "links": {
        "first": "http://127.0.0.1:5000/users/friends?q=dummy&page=1&per_page=3&sort=created_at&order=desc",
        "last": "http://127.0.0.1:5000/users/friends?q=dummy&page=1&per_page=3&sort=created_at&order=desc"
    },
    "page": 1,
    "pages": 1,
    "per_page": 3,
    "total": 1,
    "data": [
        {
            "id": 2,
            "username": "dummy2",
            "email": "dummy2@dummy.com",
            "avatar_url": "http://127.0.0.1:5000/static/images/assets/default-avatar.jpg",
            "friends": [
                1
            ],
            "created_at": "1970-01-01T00:00:00.000000",
            "updated_at": "1970-01-01T00:00:00.000000"
        }
    ]
}
```

## PATCH **UserFriendsResource**

```http
http://127.0.0.1:5000/users/friends/username
```

*Add a friend to a user's profile.*

| **Headers** | |
| --- | --- |
| **Authorization** | Bearer "user-token-here" |

### Example Request

```bash
curl --location --request PATCH 'http://127.0.0.1:5000/users/friends/dummy2' \
--header 'Authorization: Bearer <token-here>'
```

### Example Response

```json
{
    "id": 1,
    "username": "dummy",
    "email": "dummy0@dummy.com",
    "avatar_url": "http://127.0.0.1:5000/static/images/avatars/ec2d85a1-4716-4724-904d-ff79130c28d4.jpg",
    "friends": [
        2,
        3,
        4
    ],
    "created_at": "1970-01-01T00:00:00.000000",
    "updated_at": "1970-01-01T00:00:00.000000"
}
```

## DELETE **UserFriendsResource**

```http
http://127.0.0.1:5000/users/friends/username
```

*Remove a friend from a user's profile.*

| **Headers** | |
| --- | --- |
| **Authorization** | Bearer "user-token-here" |

### Example Request

```bash
curl --location --request DELETE 'http://127.0.0.1:5000/users/friends/dummy2' \
--header 'Authorization: Bearer <token-here>'
```

### Example Response

```json
{
    "id": 1,
    "username": "dummy",
    "email": "dummy0@dummy.com",
    "avatar_url": "http://127.0.0.1:5000/static/images/avatars/ec2d85a1-4716-4724-904d-ff79130c28d4.jpg",
    "friends": [
        3,
        4
    ],
    "created_at": "1970-01-01T00:00:00.000000",
    "updated_at": "1970-01-01T00:00:00.000000"
}
```

## POST **TokenResource**

```http
http://127.0.0.1:5000/token
```

*Get an user's access and refresh token.*

### Body

```json
{
    "email": "dummy@dummy.com",
    "password": "123"
}
```

### Example Request

```bash
curl --location --request POST 'http://127.0.0.1:5000/token' \
--data-raw '{
    "email": "dummy@dummy.com",
    "password": "123"
}'
```

### Example Response

```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```

## POST **RefreshToken**

```http
http://127.0.0.1:5000/refresh
```

*Get an user's access token using a refresh token.*

| **Headers** | |
| --- | --- |
| **Authorization** | Bearer "user-token-here" |

### Example Request

```bash
curl --location --request POST 'http://127.0.0.1:5000/refresh' \
--header 'Authorization: Bearer <token-here>'
```

### Example Response

```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```

## POST **RefreshToken**

```http
http://127.0.0.1:5000/revoke
```

*Blacklist an user's access token.*

| **Headers** | |
| --- | --- |
| **Authorization** | Bearer "user-token-here" |

### Example Request

```bash
curl --location --request POST 'http://127.0.0.1:5000/revoke' \
--header 'Authorization: Bearer <token-here>'
```

### Example Response

```json
{
    "msg": "Successfully logged out"
}
```
