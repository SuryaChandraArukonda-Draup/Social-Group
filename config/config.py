from flask_mongoengine import MongoEngine
from rq import Queue
from redis import Redis
from celery import Celery


queue = Queue('q', connection=Redis())


db = MongoEngine()


def initialize_db(app):
    db.init_app(app)


