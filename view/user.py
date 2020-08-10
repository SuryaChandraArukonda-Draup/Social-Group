from flask import request, Response
from models.models import User
from flask_restful import Resource
from werkzeug.security import generate_password_hash
from auth.auth import auth


# create user


class SignUpAPI(Resource):  # body : { "username" : "surya", "password" : "chandra", "email": "suryaarukonda@gmail.com"}
    def post(self):
        try:
            body = request.get_json()
            body['password'] = generate_password_hash(body['password'])
            user = User(**body).save()
            user_id = user.id
            return {'user_id': str(user_id)}, 200
        except:
            return "username and email should be unique, try again", 500


class GetUserAPI(Resource):
    @auth.login_required
    def get(self):
        user = request.authorization
        uid = User.objects(name=user['username']).to_json()

        return Response(uid, mimetype="application/json", status=200)


class DeleteUserAPI(Resource):
    @auth.login_required
    def delete(self):
        user = request.authorization  # this gives dict
        uid = User.objects.get(username=user['username'])  # this gives user object
        # user_id = str(uid.id)  # this gives the user id in string format
        try:
            if uid:
                uid.delete()
                return "User has been deleted", 200
        except:
            return "You don't belong to this database", 200


class EditUserAPI(Resource):
    # body will have change_user_name  : { "change_user_name" : "username"}, if you want to change only name
    @auth.login_required
    def put(self):
        a = request.authorization  # this gives dict
        user = User.objects.get(username=a['username'])  # this gives user object
        body = request.get_json()
        try:
            if user:
                user.update(set__username=body['change_user_name'])
                body['password'] = generate_password_hash(body['password'])
                user.update(set__password=body['password'])
                user.update(set__email=body['email'])

                return "User details changed successfully", 200
            else:
                return "User doesn't exist", 200
        except:
            return "You don't belong to this database", 200



