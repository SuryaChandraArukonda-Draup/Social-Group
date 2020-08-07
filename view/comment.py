from flask import request
from models.models import User, Group, Comment
from flask_restful import Resource
from bson import ObjectId
from datetime import datetime
from mail.mail import send_email
from config.config import queue
from auth.auth import auth
from que_task.que import printhello

# create comment


class CommentAPI(Resource):   # body contains { "content" : "comment"}
    @auth.login_required
    def post(self, gid, pid):
        u = request.authorization  # this gives dict
        uid = User.objects.get(username=u['username'])  # this gives user object
        user_id = str(uid.id)  # this gives the user id in string format
        body = request.get_json()
        user = User.objects.get(id=user_id)
        group = Group.objects.get(id=gid)
        if user_id in group.role_dict:
            comment = Comment(**body, post_id=ObjectId(pid))
            comment.date_created = datetime.now()
            comment.save()
            # update last active status for user
            temp_dict = group.last_active_dict
            temp_dict[user_id] = datetime.now()
            group.update(set__last_active_dict=temp_dict)
            content = "{name} has posted a comment today".format(name=user.username)
            queue.enqueue(printhello())  # this is just a check that q works
            queue.enqueue(send_email, user.email, content)
            # queue.enqueue(send_email(user.email, content))
            # send_email(user.email, content)
            return {'comment_id': str(comment.id)}, 200
        else:
            return "You ain't a member of this group", 200


class DeleteCommentAPI(Resource):
    # only post_owner, admin and moderator can delete
    @auth.login_required
    def delete(self, gid, cid):
        user = request.authorization  # this gives dict
        uid = User.objects.get(username=user['username'])  # this gives user object
        user_id = str(uid.id)  # this gives the user id in string format
        comment = Comment.objects.get(id=cid)
        group = Group.objects.get(id=gid)
        try:
            role = group.role_dict[user_id]
            comments = Comment.objects(user_id=user_id)
            if comment in comments or role == 'ADMIN' or role == 'MODERATOR':
                comment.delete()
                return "Comment deleted", 200
            else:
                return "You don't have the permission required", 200
        except:
            return "You ain't a member of the group", 200


