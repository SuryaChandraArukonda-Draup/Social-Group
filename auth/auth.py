from models.models import User
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if User.objects.filter(username=username).first():
        user = User.objects.filter(username=username).first()
        if check_password_hash(user.password, password):
            return True


'''
@auth.verify_password
def verify_password(username, password):
    if User.objects(username=username) and User.objects(password=password):
        return username
'''
