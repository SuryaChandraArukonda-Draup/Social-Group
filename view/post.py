from flask import request, Response
from models.models import Group, Post, User
from flask_restful import Resource
from bson import ObjectId
from datetime import datetime
from auth.auth import auth
from constants.constants import A, MD, M
from que_task.que import printhello
from mail.mails import send_mail
from config.config import queue


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
            recipients = []
            # update last active status for user
            temp_dict = group.last_active_dict
            temp_dict[user_id] = datetime.now()
            group.update(set__last_active_dict=temp_dict)

            for x in group.role_dict:
                if group.role_dict[x] == A or group.role_dict[x] == MD:
                    u = User.objects.get(id=x)
                    if u:
                        recipients.append(u.email)

            if group.role_dict[user_id] == M:
                content = "{name} wants to put a post, please accept his request!".format(name=user.username)
                queue.enqueue(printhello())  # this is just a check that q works
                queue.enqueue(send_mail, recipients, content)

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
            if post in posts or role == A or role == MD:
                post.delete()
                return "Post deleted", 200
            else:
                return "You don't have the permission to post", 200
        except:
            return "You are no longer member of this group", 200


class GetPostAPI(Resource):
    @auth.login_required
    def get(self, gid, pid):
        user = request.authorization
        uid = User.objects.get(username=user['username'])
        uid = str(uid.id)

        try:
            group = Group.objects.get(id=gid)
            if uid in group.role_dict:

                post = Post.objects.get(id=pid).to_json()

                return Response(post, mimetype="application/json", status=200)

            else:
                return "You are not member of the group", 500
        except:
            return "Invalid group or post id", 500


class EditPostAPI(Resource):
    # body will have change_post_name  : { "change_post_name" : "post"}
    @auth.login_required
    def put(self, gid, pid):
        admin = request.authorization  # this gives dict
        admin_name = User.objects.get(username=admin['username'])  # this gives user object
        uid = str(admin_name.id)  # this gives the admin id in string format
        body = request.get_json()
        try:
            group = Group.objects.get(id=gid)
            if uid in group.role_dict:
                post = Post.objects.get(id=pid).to_json()

                post.update(set__content=body['change_post_content'])

                temp_dict = group.last_active_dict
                temp_dict[uid] = datetime.now()
                group.update(set__last_active_dict=temp_dict)

                return "Post content changed successfully", 200
            else:
                return "You are not a member if this group", 200
        except:
            return "Post doesn't belong this group", 200
