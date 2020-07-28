from config.config import db


class User(db.Document):
    name = db.StringField(required=True, max_length=30)
    email = db.StringField(required=True)
    posts = db.ListField(db.ReferenceField('Post', reverse_delete_rule=db.PULL))      # ids of post created by the user
    comments = db.ListField(db.ReferenceField('Comment', reverse_delete_rule=db.PULL))


class Role(db.Document):
    name = db.StringField(required=True, unique=True, max_length=50)
    permissions = db.ListField(db.StringField())


class Group(db.Document):
    name = db.StringField(required=True, max_length=30)
    visibility = db.StringField(default='public')
    posts = db.ListField(db.ReferenceField('Post'), reverse_delete_rule=db.PULL)
    users = db.ListField(db.DictField())        # fill with {'user_id':'role_id'}


class Post(db.Document):
    user_id = db.ReferenceField('User')
    group_id = db.ReferenceField('Group')
    content = db.StringField(required=True, max_length=200)
    # approval is set to true for now
    approval = db.StringField(Default=True, max_length=10)


class Comment(db.Document):
    user_id = db.ReferenceField('User')
    post_id = db.ReferenceField('Post')
    content = db.StringField(required=True, max_length=75)

# one to many relation 1 user can have lot of comments and posts



