from flask import Flask
from config.config import initialize_db
from flask_restful import Api
from url.url import initialize_routes
from errors import errors

app = Flask(__name__)


api = Api(app, errors=errors)


app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/SocialGroup'
}

initialize_db(app)
initialize_routes(api)