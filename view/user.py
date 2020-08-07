from flask import request
from models.models import User
from flask_restful import Resource
from werkzeug.security import generate_password_hash


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
            return "username should be unique try again", 500





