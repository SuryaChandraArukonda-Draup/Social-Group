from datetime import datetime, timedelta
from models.models import Group


def inactive_users():

    present_time = datetime.now()
    groups = Group.objects()
    for group in groups:
        temp_role_dict = {}
        temp_role_dict.update(group.role_dict)
        temp_last_active_dict = {}
        temp_last_active_dict.update(group.last_active_dict)
        for user_id, last_active in group.last_active_dict.items():
            if last_active < present_time-timedelta(minutes=1) and group.role_dict[user_id] != 'ADMIN':
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

    print('Scheduler is working')
    return ""