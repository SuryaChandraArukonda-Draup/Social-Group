from Project.config.config import db


class Permissions(db.Document):
    # id
    name = db.StringField(required=True, unique=True)


class Roles(db.Document):
    name = db.StringField(required=True, unique=True, default='member')
    permission = db.ListField(db.StringField(), required=True)      # list of permission_id


class Group(db.Document):
    # id
    name = db.StringField(required=True, max_length=30)
    visibility = db.StringField(default='public')
    users = db.DictField()    # all the users in group {'user_id':'role_id'}


class User(db.Document):
    # id
    name = db.StringField(required=True, max_length=25)
    email = db.StringField(required=True, unique=True)
    groups = db.ListField(db.StringField())      # ids of groups user is connected
    posts = db.ListField(db.StringField())      # ids of post created by the user
    comments = db.ListField(db.StringField())      # ids of comments created by the user


class Post(db.Document):
    # id
    user_id = db.StringField(required=True)
    group_id = db.StringField(required=True)
    content = db.StringField(required=True, max_length=200)
    approval = db.StringField(Default=False, max_length=25)


class Comment(db.Document):
    # id
    user_id = db.StringField(required=True)
    post_id = db.StringField(required=True)
    content = db.StringField(required=True, max_length=80)

