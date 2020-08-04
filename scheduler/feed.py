from datetime import datetime, timedelta
from mongoengine import Q
from models.models import Group, Post, User
from mail.mail import send_email


def dailyfeed():
    # time now is given such that its mid night
    time_now = datetime.now()
    last_day = time_now - timedelta(hours=24)
    groups = Group.objects()
    for group in groups:
        posts = Post.objects(Q(groupid=group.id) & Q(date_created__lte=time_now) & Q(date_created__gte=last_day))
        total = len(posts)
        content = '{total} posts were put today'.format(total=total)
        recipients = []
        for user_id, access in group.role_dict.items():
            if access == 'ADMIN' or access == 'MODERATOR':
                user = User.objects(id=user_id)
                recipients.append(user)
        # send_email(recipients, text_body), structure of send_email
        send_email(recipients, content)
