from datetime import datetime, timedelta
from mongoengine import Q, connect
from rq import Queue
from redis import Redis
from models.models import Group, Post, User
from mail.mails import send_mail
from constants.constants import A, MD, S

sch_queue = Queue('test', connection=Redis())


def dailyfeed():
    # time now is given such that its mid night

    connect(S)
    print("working")

    time_now = datetime.now()
    last_day = time_now - timedelta(hours=24)
    groups = Group.objects()
    for group in groups:
        posts = Post.objects(Q(group_id=group.id) & Q(date_created__lte=time_now) & Q(date_created__gte=last_day))
        if posts:
            total = len(posts)
            content = '{total} posts were put today'.format(total=total)
            recipients = []
            for user_id, access in group.role_dict.items():
                if access == A or access == MD:
                    user = User.objects.get(id=user_id)
                    recipients.append(user.email)
            sch_queue.enqueue(send_mail, recipients, content)
