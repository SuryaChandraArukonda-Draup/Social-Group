from flask import Flask
from flask_mail import Mail
from config.config import initialize_db
from flask_restful import Api
from url.url import initialize_routes

app = Flask(__name__)
api = Api(app)
mail = Mail(app)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/SocialGroup'
}

initialize_db(app)
initialize_routes(api)


app.run(debug=True)
