# Using Images

If we want to add a profile image to our users, we are going to need to let them upload images to our servers. The user model will now contain a path to its avatar image stored on our application server. We will also use the [Pillow](https://pillow.readthedocs.io/en/stable/) library to compress uploaded images in order to reduce the stress on our server and therefore enhance the performance of our API.

## User Avatar

The user model is going to need a new attribute in order to store the path to its avatar image. When our API gets a request for the avatar image, we will find the file path and generate a new URL to point to the image location on the server and return it to the client.

Hence, we modify the user model as such:

```python
avatar_image = db.Column(db.String(100), default=None)
```

We then run the following commands to update the database:

```zsh
flask db migrate
flask db upgrade
```

## Flask-Uploads

[Flask-Uploads](https://pythonhosted.org/Flask-Uploads/) simplify the development of the file upload function. It can handle several common file types out of the box like images, documents or audio files.

In order to upload a file, we need to define an image upload set as follow:

```python
image_set = UploadSet('images', IMAGES)
```

We can then save an image from an incoming HTTP request like so:

```python
image_set.save(image, folder=folder, name=filename)
```

We also need to store the upload set in our app:

```python
configure_uploads(app, image_set)
```

In our case, we will store the images under `static/images/avatars`.

NB: Flask-Uploads has not been updated to conform to the updated [Werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/) API changes. We use [Flask-Reuploaded](https://github.com/jugmac00/flask-reuploaded) as a drop-in replacement.

Once our image_set has been registered with our app, we can update the marshmallow user schema as such:

```python
avatar_url = fields.Method(serialize='dump_avatar_url')

def dump_avatar_url(self, user: User):
        if user.avatar_image:
            return url_for('static', filename='images/avatars/{}'.format(user.avatar_image), _external=True)
        else:
            return url_for('static', filename='images/assets/default-avatar.jpg', _external=True)
```

Note that we also specify a default user avatar so that a new registered user has a default avatar.

Once our schema has been modified, we can define a small helper function to save an image with an unique filename:

```python
def save_image(image, folder: str) -> str:
    filename = '{}.{}'.format(uuid.uuid4(), extension(image.filename))
    image_set.save(image, folder=folder, name=filename)

    return filename
```

And then use it in a new resource **UserAvatarUploadResource** used to upload images:

```python
class UserAvatarUploadResource(Resource):
    @jwt_required
    def put(self):
        file = request.files.get('avatar')

        if not file:
            return {'msg': 'not a valid image'}, HTTPStatus.BAD_REQUEST

        if not image_set.file_allowed(file, file.filename):
            return {'msg': 'file type not allowed'}, HTTPStatus.BAD_REQUEST

        user = User.get_by_id(id=get_jwt_identity())

        if user.avatar_image:
            avatar_path = image_set.path(folder='avatars', filename=user.avatar_image)
            if os.path.exists(avatar_path):
                os.remove(avatar_path)

        filename = save_image(image=file, folder='avatars')

        user.avatar_image = filename
        user.save()

        return user_avatar_schema.dump(user), HTTPStatus.OK
```

Finally, we register this new route in our app:

```python
api.add_resource(UserAvatarUploadResource, '/users/avatar')
```

## Image Resizing and Compression

In order to enhance the performance of our API, we can resize and compress the images uploaded by the client as such:

```python
def save_image(image, folder: str) -> str:
    filename = '{}.{}'.format(uuid.uuid4(), extension(image.filename))
    image_set.save(image, folder=folder, name=filename)

    filename = compress_image(filename=filename, folder=folder)

    return filename

def compress_image(filename, folder):
    file_path = image_set.path(filename=filename, folder=folder)

    image = Image.open(file_path)

    if image.mode != "RGB":
        image = image.convert("RGB")

    if max(image.width, image.height) > 1600:
        maxsize = (1600, 1600)
        image.thumbnail(maxsize)

    compressed_filename = '{}.jpg'.format(uuid.uuid4())
    compressed_file_path = image_set.path(filename=compressed_filename, folder=folder)

    image.save(compressed_file_path, optimize=True, quality=85)

    os.remove(file_path)

    return compressed_filename
```
