from flask import request, Response
from models.models import Group, Post, User, DeletedUsers
from flask_restful import Resource
from datetime import datetime
from auth.auth import auth


# create group

class GroupAPI(Resource):
    # body : { "name" : "group1", "visibility" : "private"}
    @auth.login_required
    def post(self):
        body = request.get_json()
        user = request.authorization  # this gives dict
        uid = User.objects.get(username=user['username'])  # this gives user object
        user_id = str(uid.id)  # this gives the user id in string format
        name = body['name']
        if body['visibility']:
            visibility = body['visibility']
        else:
            visibility = 'public'
        group = Group(name=name, visibility=visibility)
        group.role_dict[user_id] = 'ADMIN'
        group.save()
        return {'group_id': str(group.id)}, 200

# Add a member to existing group


class AddToGroupAPI(Resource):
    # body : { "role_dict" : {"new_user_id":"role"} }
    # only ADMIN can add user
    @auth.login_required
    def put(self, gid):
        body = request.get_json()
        admin = request.authorization  # this gives dict
        admin_name = User.objects.get(username=admin['username'])  # this gives user object
        uid = str(admin_name.id)  # this gives the admin id in string format
        role_dict = body['role_dict']  # dict with {'user_id':'role'}
        new_user_id = list(role_dict.keys())[0]
        group = Group.objects.get(id=gid)
        role_dict.update(group.role_dict)
        temp_dict = group.last_active_dict
        # this temp dict is for last active update
        if uid in group.role_dict and group.role_dict[uid] == 'ADMIN':
            group.update(set__role_dict=role_dict)
            temp_dict[new_user_id] = datetime.now()
            group.update(set__last_active_dict=temp_dict)
            return "User admitted successfully", 200
        else:
            return "Admin access denied"


class RemoveUserGroupAPI(Resource):
    # body will have del_user_id i.e; id of user to be removed : { "del_user_id" : ""}
    # only ADMIN can remove user
    @auth.login_required
    def put(self, gid):
        admin = request.authorization  # this gives dict
        admin_name = User.objects.get(username=admin['username'])  # this gives user object
        uid = str(admin_name.id)  # this gives the admin id in string format
        body = request.get_json()
        group = Group.objects.get(id=gid)
        try:
            if group.role_dict[uid] == 'ADMIN':
                del_user = body['del_user_id']
                DeletedUsers(group_id=gid, deleted_user_ids=body['del_user_id']).save()
                role_dict = group.role_dict
                last_active_dict = group.last_active_dict
                for key in list(role_dict):
                    if key == del_user:
                        del role_dict[del_user]
                        break
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


class ReadGroupAPI(Resource):
    # read group contents based on access offered by group i.e. public or private
    @auth.login_required
    def get(self, gid):
        user = request.authorization  # this gives dict
        uid = User.objects.get(name=user['username'])  # this gives user object
        user_id = str(uid.id)  # this gives the user id in string format
        group = Group.objects.get(id=gid)

        if group.visibility == 'public':
            posts = Post.objects(group_id=gid).to_json()
            return Response(posts, mimetype="application/json", status=200)
        elif user_id in group.role_dict:
            posts = Post.objects(group_id=gid).to_json()
            return Response(posts, mimetype="application/json", status=200)
        else:
            return "You do not have the required access", 200
