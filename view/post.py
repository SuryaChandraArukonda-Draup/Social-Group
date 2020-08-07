from flask import request
from models.models import Group, Post, User
from flask_restful import Resource
from bson import ObjectId
from datetime import datetime
from auth.auth import auth


# create post


class PostAPI(Resource):     # body : { "content" : "post"}
    # Only group users can post
    @auth.login_required
    def post(self, gid):
        body = request.get_json()
        user = request.authorization  # this gives dict
        uid = User.objects.get(username=user['username'])  # this gives user object
        user_id = str(uid.id)  # this gives the user id in string format
        group = Group.objects.get(id=gid)
        if user_id in group.role_dict:
            post = Post(**body, group_id=ObjectId(gid))
            post.date_created = datetime.now()
            post.save()
            # group id is a reference field and rf only takes object id.
            # convert object id to string with str when required
            post_id = post.id
            # update last active status for user
            temp_dict = group.last_active_dict
            temp_dict[user_id] = datetime.now()
            group.update(set__last_active_dict=temp_dict)

            return {'post_id': str(post_id)}, 200
        else:
            return "You ain't a member of this group", 200


class DeletePostAPI(Resource):     # body contains user_id and only post owner(member), admin or moderator can delete
    @auth.login_required
    def delete(self, gid, pid):
        user = request.authorization  # this gives dict
        uid = User.objects.get(username=user['username'])  # this gives user object
        user_id = str(uid.id)  # this gives the user id in string format
        post = Post.objects.get(id=pid)
        group = Group.objects.get(id=gid)
        try:
            role = group.role_dict[user_id]
            posts = Post.objects(user_id=user_id)
            if post in posts or role == 'ADMIN' or role == 'MODERATOR':
                post.delete()
                return "Post deleted", 200
            else:
                return "You don't have the permission to post", 200
        except:
            return "You are no longer member of this group", 200
