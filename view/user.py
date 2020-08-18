from flask import request, Response
from models.models import User, SudoUser
from flask_restful import Resource
from werkzeug.security import generate_password_hash
from auth.auth import auth
from flask_mongoengine import Pagination
import json
import celery
from mail.mail import send_mail


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


'''class GetUserAPI(Resource):
    @auth.login_required
    def get(self):
        user = request.authorization
        uid = User.objects(name=user['username']).to_json()

        return Response(uid, mimetype="application/json", status=200)'''


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


class GetAllUserApi(Resource):
    @auth.login_required
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


class GetUserApi(Resource):
    @auth.login_required
    @celery.task
    def get(self):
        user = request.authorization
        uid = User.objects(username=user['username']).to_json()
        user = User.objects.get(username=user['username'])
        # testing celery by sending a mail asynchronously
        content = "celery test mail"
        subject = "celery test"
        # task = send_mail.delay(content,[user.email],subject)
        task = send_mail.apply_async(args=[content, user.email, subject], countdown=60)
        return Response(uid, mimetype="application/json", status=200)
