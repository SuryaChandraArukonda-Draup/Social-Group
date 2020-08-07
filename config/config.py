from flask_mongoengine import MongoEngine
from rq import Queue
from redis import Redis

queue = Queue('q', connection=Redis())

db = MongoEngine()

'''def schedule_tasks(function_to_execute, duration, freq):

    scheduler_tasks.schedule(
        scheduled_time=datetime.utcnow(),            # Time for first execution, datetime.min for 00:00
        func=function_to_execute(),                     # Function to be queued
        args=[],             # Arguments passed into function when executed
        kwargs={},         # Keyword arguments passed into function when executed, eg: kwargs={'foo': 'bar'}
        interval=duration,             # Time before the function is called again, in seconds
        repeat=freq,                     # Repeat this number of times (None means repeat forever)
        meta={}            # Arbitrary pickleable data on the job itself eg: meta={'foo': 'bar'}
    )
'''


def initialize_db(app):
    db.init_app(app)
