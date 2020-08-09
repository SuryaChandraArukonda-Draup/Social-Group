from flask import request, Response
from models.models import Group, Post, User, DeletedUsers
from flask_restful import Resource
from datetime import datetime
from auth.auth import auth
from constants.constants import A, MD, P


# create group

class GroupAPI(Resource):
    # body : { "name" : "group1", "visibility" : "private"}
    @auth.login_required
    def post(self):
        body = request.get_json()
        user = request.authorization  # this gives dict
        uid = User.objects.get(username=user['username'])  # this gives user object
        user_id = str(uid.id)  # this gives the user id in string format
        try:
            name = body['name']
            if body['visibility']:
                visibility = body['visibility']
            else:
                visibility = P
            group = Group(name=name, visibility=visibility)
            group.role_dict[user_id] = A
            group.save()
            return {'group_id': str(group.id)}, 200
        except:
            return "Name already exists"

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
        if uid in group.role_dict:  # and group.role_dict[uid] == A and group.role_dict[uid] == MD
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
            if group.role_dict[uid] == A:
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


class GetGroupAPI(Resource):

    @auth.login_required
    def get(self, gid):
        user = request.authorization
        uid = User.objects.get(name=user['username'])
        uid = str(uid.id)
        try:
            group = Group.objects.get(id=gid)
            if uid in group.role_dict:
                group = Group.objects(id=gid).to_json()
                return Response(group, mimetype="application/json", status=200)
            else:
                return "You are not member of the group", 500
        except Exception as exception:
            return exception


class ChangeRoleApi(Resource):
    # only admin can change role
    @auth.login_required
    def put(self, gid):

        # body contains dict of person whose role is changed {"user id":"new role"}
        user = request.authorization
        uid = User.objects.get(name=user['username'])
        uid = str(uid.id)

        body = request.get_json()

        group = Group.objects(id=gid).get()
        try:
            if group.role_dict[uid] == A:
                role_dict = group.role_dict
                role_dict.update(body['change_role'])
                group.update(set__role_dict=role_dict)
                return "Role changed successfully", 200
            else:
                return "You are not an admin", 200
        except:
            return "You are not member of the group", 200


class DeleteGroupAPI(Resource):
    @auth.login_required
    def delete(self, gid):
        user = request.authorization  # this gives dict
        uid = User.objects.get(username=user['username'])  # this gives user object
        user_id = str(uid.id)  # this gives the user id in string format
        group = Group.objects.get(id=gid)
        try:
            role = group.role_dict[user_id]
            if role == A or role == MD:
                group.delete()
                return "Group has been deleted", 200
            else:
                return "You don't have the permission to delete this group", 200
        except:
            return "You are not an admin or moderator of this group", 200


class EditGroupAPI(Resource):
    # body will have change_group_name  : { "change_group_name" : "group2"}
    @auth.login_required
    def put(self, gid):
        admin = request.authorization  # this gives dict
        admin_name = User.objects.get(username=admin['username'])  # this gives user object
        uid = str(admin_name.id)  # this gives the admin id in string format
        body = request.get_json()
        group = Group.objects.get(id=gid)
        try:
            if group.role_dict[uid] == A or group.role_dict[uid] == MD:
                change_group_name = body['change_group_name']
                group.update(set__name=change_group_name)

                if group.role_dict[uid] == A:
                    group.update(set__visibility=body['visibility'])
                    return "Visibility changed by Admin"

                temp_dict = group.last_active_dict
                temp_dict[uid] = datetime.now()
                group.update(set__last_active_dict=temp_dict)

                return "Group name changed successfully", 200
            else:
                return "You are not an ADMIN or MODERATOR", 200
        except:
            return "You are not a member of this group", 200

