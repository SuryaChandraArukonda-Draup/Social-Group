from flask_mongoengine import MongoEngine
from rq import Queue
from redis import Redis
from rq_scheduler import Scheduler

scheduler = Scheduler(connection=Redis())
queue = Queue(connection=Redis())

db = MongoEngine()


def initialize_db(app):
    db.init_app(app)

