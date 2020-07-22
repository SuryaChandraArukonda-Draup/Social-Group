from flask import request
from Project.models.models import Permissions, User, Roles, Group, Post, Comment
from flask_restful import Resource


class Permissions1(Resource):
    def post(self):
        body = request.get_json()
        permission = Permissions(**body).save()
        permission_id = permission.id
        return {'permission_id': str(permission_id)}, 200


# add role


class Role1(Resource):
    def get(self):
        body = request.get_json()
        role = Roles(**body).save()
        role_id = role.id
        return {'role_id': str(role_id)}, 200


# create group

class Group1(Resource):
    def post(self):
        body = request.get_json()
        group = Group(**body).save()
        group_id = group.id
        return {'group_id': str(group_id)}, 200


# create user


class User1(Resource):
    def post(self):
        body = request.get_json()
        user = User(**body).save()
        user_id = user.id
        return {'user_id': str(user_id)}, 200


# create post


class Post1(Resource):
    def post(self):
        body = request.get_json()
        post = Post(**body).save()
        post_id = post.id
        return {'post_id': str(post_id)}, 200


# create comment


class Comment1(Resource):
    def post(self):
        body = request.get_json()
        comment = Comment(**body).save()
        comment_id = comment.id
        return {'comment_id': str(comment_id)}, 200
