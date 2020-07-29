from config.config import scheduler


def schedule_tasks(first_execution, function_to_execute, duration, freq):

    scheduler.schedule(
        scheduled_time=first_execution,            # Time for first execution, datetime.min for 00:00
        func=function_to_execute(),                     # Function to be queued
        args=[],             # Arguments passed into function when executed
        kwargs={},         # Keyword arguments passed into function when executed, eg: kwargs={'foo': 'bar'}
        interval=duration,             # Time before the function is called again, in seconds
        repeat=freq,                     # Repeat this number of times (None means repeat forever)
        meta={}            # Arbitrary pickleable data on the job itself eg: meta={'foo': 'bar'}
    )