from flask import request
from models.models import User, Roles, Group, Post, Comment
from flask_restful import Resource
from bson import ObjectId


# add role


class Role1(Resource):
    def get(self):
        body = request.get_json()
        role = Roles(**body).save()
        role_id = role.id
        return {'role_id': str(role_id)}, 200


# create group

class Group1(Resource):

    def post(self, id):
        # id is the user_id of group creator
        body = request.get_json()
        group = Group(**body)
        group.users = [{id:'ADMIN'}]
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
    def post(self, id):
        # id is group id and body contains Post class contents
        body = request.get_json()
        user_id = body['user_id']
        group = Group.objects.get(id=id)
        for user in group.users:
            if user_id in user:
                post = Post(**body, groupid=ObjectId(id)).save()
                # group id is a reference field and rf only takes object id.
                # convert object id to string with str when required
                post_id = post.id
                # change user list
                User.objects(id=user_id).update_one(push__posts=post)
                # change group list
                group.update(push__posts=post)
                return {'post_id': str(post_id)}, 200
        return 'You are not a member of the group'


# create comment


class Comment1(Resource):

    # create comment and update in user list
    # / api /<gid>/<pid>/comment
    def post(self, gid, pid):
        # gid is group id,pid post id and body contains Comment class contents
        body = request.get_json()
        user_id = body['user_id']
        group = Group.objects.get(id=gid)
        for user in group.users:
            if user_id in user:
                comment = Comment(**body, postid=ObjectId(pid)).save()
                # post id is a reference field and rf only takes object id.
                # convert object id to string with str when required
                comment_id = comment.id
                # change user list
                User.objects(id=user_id).update_one(push__comments=comment)
                return {'comment_id': str(comment_id)}, 200
        return 'You are not a member of the group'

# Add a member to existing group


class AddToGroup1(Resource):

    # push user to the group by roles who have add rights
    def put(self, id):
        # id is group id here
        # body will have user_id of both admin and new join
        body = request.get_json()
        user_id = body['user_id']
        new_user = body['new_user']     # dict with {'user_id':'role'}
        group = Group.objects.get(id=id)
        for user in group.users:
            if user_id in user:
                permission = Roles.objects.get(name=user[user_id])
                permission = permission.permissions
                if 'ADDUSER' in permission:
                    group.update(push__users=new_user)
                    return 'User added successfully'
                else:
                    return "You don't have add user rights"

        return 'Person adding user is not a member of the group'


class RemoveGroup1(Resource):

    # pull user from the group by roles who have remove from group rights
    def put(self, id):
        # id is group id here
        # body will have user_id of both admin and user to be deleted
        body = request.get_json()
        user_id = body['user_id']
        del_user = body['del_user']             # dict with {'user_id':'role'}
        group = Group.objects.get(id=id)
        for user in group.users:
            if user_id in user:
                permission = Roles.objects.get(name=user[user_id])
                permission = permission.permissions
                if 'DELUSER' in permission:
                    group.update(pull__users=del_user)
                    return 'User Removed successfully'
                else:
                    return "You don't have delete user rights"

        return 'Person removing user is not a member of the group'



