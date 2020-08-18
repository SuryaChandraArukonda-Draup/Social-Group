from models.models import Post, User
from mongoengine import connect
from flask import request, Response
from flask_restful import Resource
from marshmallow import Schema, fields
from flask_paginate import Pagination
import json

connect("SocialGroup")
posts = Post.objects()

for post in posts:
    print(post.content)
dir(posts)


class SudoUser(Schema):
    name = fields.Str()
    password = fields.Str()
    email = fields.Str()


class GetAllUserApi(Resource):

    def get(self, page_no):
        users = User.objects()
        # The pagination method returns non json pagination object
        users = Pagination(users, page=int(page_no), per_page=2)
        # this gives list of user object
        users = users.items
        # using marshmallow to serialize
        obj = SudoUser(many=True)
        users = obj.dump(users)
        # using dumps to convert to json object
        users = json.dumps(users)
        # print(users)
        return Response(users, mimetype="application/json", status=200)
