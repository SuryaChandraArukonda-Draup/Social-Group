from celery import Celery
from flask import Flask
from redis import Redis
from rq import Queue
from flask_mail import Mail
from flask_restful import Api
from flask_mongoengine import MongoEngine
from url.url import initialize_routes

app = Flask(__name__)
# print

api = Api(app)
mail = Mail(app)

queue = Queue('test', connection=Redis())

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/SocialGroup'
}

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['CELERY_IMPORTS'] = 'mail.mail'


celery = Celery(app.name)
# This config is for simple task execution
celery.conf.update(
    result_backend=app.config["CELERY_RESULT_BACKEND"],
    broker_url=app.config["CELERY_BROKER_URL"],
    imports=app.config["CELERY_IMPORTS"],
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)


# This config is for running with the beat scheduler
# # Add periodic tasks
# celery_beat_schedule = {
#   "time_scheduler": {
#       "task": "mail.mails.send_mail",
#       # Run every minute and half
#       "schedule": 90,
#       "args":('test mail',['dev.aakash1794@gmail.com'],'celery working'),
#   }
# }
# celery.conf.update(
#     result_backend=app.config["CELERY_RESULT_BACKEND"],
#     broker_url=app.config["CELERY_BROKER_URL"],
#     imports=app.config["CELERY_IMPORTS"],
#     timezone="UTC",
#     task_serializer="json",
#     accept_content=["json"],
#     result_serializer="json",
#     beat_schedule=celery_beat_schedule,
# )


# celery -A config.celery worker

db = MongoEngine()


def initialize_db(ap):
    db.init_app(ap)


initialize_db(app)
initialize_routes(api)

app.run(debug=True)
