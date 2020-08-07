from redis import Redis
from rq_scheduler import Scheduler
from scheduler_tasks.delete_inactive import inactive_users
from scheduler_tasks.feed import dailyfeed

scheduler = Scheduler(connection=Redis())

cron_string = "* * * * *"       # every minute

scheduler.cron(
    cron_string,
    func=dailyfeed,  # Function to be queued
    repeat=1,  # Repeat this number of times (None means repeat forever)
    queue_name='test',  # In which queue the job should be put in
    use_local_timezone=True  # Interpret hours in the local timezone
 )


'''cron_string = "* * * * *"       # every minute

scheduler.cron(
    cron_string,
    func=inactive_users,  # Function to be queued
    repeat=0,  # Repeat this number of times (None means repeat forever)
    queue_name='test',  # In which queue the job should be put in
    use_local_timezone=True  # Interpret hours in the local timezone
)'''