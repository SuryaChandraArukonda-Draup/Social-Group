from flask import request, Response
from models.models import User, Roles, Group, Post, Comment
from flask_restful import Resource
from bson import ObjectId
from datetime import datetime


# create group

class Group1(Resource):

    def post(self):
        # body has id of group creator
        body = request.get_json()
        user_id = body['user_id']
        name = body['name']  # check once
        if body['visibility']:
            visibility = body['visibility']
        else:
            visibility = 'public'
        group = Group(name=name, visibility=visibility)
        group.role_dict[user_id] = 'ADMIN'
        group.save()
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

    # Only group users can post

    def post(self, gid):
        # body contains user id,content
        body = request.get_json()
        group = Group.objects.get(id=gid)
        if body['user_id'] in group.role_dict:
            post = Post(**body, group_id=ObjectId(gid))
            post.date_created = datetime.now()
            post.save()
            # group id is a reference field and rf only takes object id.
            # convert object id to string with str when required
            post_id = post.id
            # update last active status for user
            temp_dict = group.last_active_dict
            temp_dict[body['user_id']] = datetime.now()
            group.update(set__last_active_dict=temp_dict)

            return {'post_id': str(post_id)}, 200
        else:
            return "You ain't a member of this group", 200


class DeletePost1(Resource):
    # only post owner, admin and moderator can delete
    def delete(self, gid, pid):
        # body contains user id
        body = request.get_json()
        post = Post.objects.get(id=pid)
        group = Group.objects.get(id=gid)
        role = group.role_dict[body['user_id']]
        if post.user_id == body['user_id'] or role == 'ADMIN' or role == 'MODERATOR':
            post.delete()
            return "Post deleted", 200
        else:
            return "You have no permission", 200


# create comment


class Comment1(Resource):

    def post(self, gid, pid):
        # body contains user_id,content
        body = request.get_json()
        user = User.objects.get(id=body['user_id'])
        group = Group.objects.get(id=gid)
        if body['user_id'] in group.role_dict:
            comment = Comment(**body, post_id=ObjectId(pid))
            comment.date_created = datetime.now()
            comment.save()
            # update last active status for user
            temp_dict = group.last_active_dict
            temp_dict[body['user_id']] = datetime.now()
            group.update(set__last_active_dict=temp_dict)
            comment_id = comment.id
            return {'comment_id': str(comment_id)}, 200
        else:
            return "You are not a member of the group", 200


class DeleteComment1(Resource):
    # only post_owner, admin and moderator can delete
    def delete(self, gid, cid):
        # body contains user_id
        body = request.get_json()
        comment = Comment.objects.get(id=cid)
        group = Group.objects.get(id=gid)
        role = group.role_dict[body['user_id']]
        if comment.userid == body['user_id'] or role == 'ADMIN' or role == 'MODERATOR':
            comment.delete()
            return "Comment deleted", 200
        else:
            return "You don't have the permission required", 200


# Add a member to existing group


class AddToGroup1(Resource):

    # only ADMIN can add user
    def put(self, gid):

        body = request.get_json()
        uid = body['user_id']
        new_user = body['new_user']  # dict with {'user_id':'role'}
        new_user_id = list(new_user.keys())[0]
        group = Group.objects.get(id=gid)
        new_user.update(group.role_dict)
        temp_dict = group.last_active_dict
        # this temp dict is for last active update
        if uid in group.role_dict and group.role_dict[uid] == 'ADMIN':
            group.update(set__role_dict=new_user)
            temp_dict[new_user_id] = datetime.now()
            group.update(set__last_active_dict=temp_dict)
            return "User admitted successfully", 200
        else:
            return "Admin access denied"


class RemoveUserGroup1(Resource):

    # only ADMIN can remove user
    def put(self, gid):
        # body will have user_id of admin and id of user to be removed

        body = request.get_json()
        uid = body['user_id']
        group = Group.objects.get(id=gid)
        try:
            if group.role_dict[uid] == 'ADMIN':
                del_user = body['del_user_id']

                role_dict = group.role_dict
                last_active_dict = group.last_active_dict
                for key in list(role_dict):
                    if key == del_user:
                        del role_dict[del_user]
                        break
                # element should be deleted in dict via this way otherwise iteration error
                for key in list(last_active_dict):
                    if key == del_user:
                        del last_active_dict[del_user]
                        break
                group.update(set__last_active_dict=last_active_dict)
                group.update(set__role_dict=role_dict)
                return "user deleted successfully", 200
            else:
                return "You are not an ADMIN", 200
        except:
            return "You are not a member of the group", 200


class ReadGroup1(Resource):
    # read group contents based on access offered by group i.e. public or private
    def get(self, gid):
        # body will have user_id of person accessing to read
        body = request.get_json()
        user_id = body['user_id']
        group = Group.objects.get(id=gid)

        if group.visibility == 'public':
            posts = Post.objects(groupid=gid).to_json()
            return Response(posts, mimetype="application/json", status=200)
        elif user_id in group.role_dict:
            posts = Post.objects(groupid=gid).to_json()
            return Response(posts, mimetype="application/json", status=200)
        else:
            return "You do not have the required access", 200
