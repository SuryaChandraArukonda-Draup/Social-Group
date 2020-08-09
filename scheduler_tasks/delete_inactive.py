from datetime import datetime, timedelta
from models.models import Group, SaveLogs
from mongoengine import connect
from constants.constants import A


def inactive_users():
    connect("SocialGroup")
    print('Scheduler working')

    present_time = datetime.now()
    groups = Group.objects()
    for group in groups:
        temp_role_dict = {}
        temp_role_dict.update(group.role_dict)
        temp_last_active_dict = {}
        temp_last_active_dict.update(group.last_active_dict)
        message_list = []
        for user_id, last_active in group.last_active_dict.items():
            if last_active < present_time - timedelta(minutes=1) and group.role_dict[user_id] != A:
                message = "{name} got deleted due to inactivity".format(name=user_id)
                message_list.append(message)

                for key in list(group.role_dict):
                    if key == user_id:
                        del temp_role_dict[user_id]
                        break
                for key in list(group.last_active_dict):
                    if key == user_id:
                        del temp_last_active_dict[user_id]
                        break
            group.update(set__last_active_dict=temp_last_active_dict)
            group.update(set__role_dict=temp_role_dict)
            SaveLogs(group_id=group, message=message_list).save()
