from mongoengine import connect
from datadump.create_data import create_user, create_group, add_user_group, add_post_comment
connect("SocialGroup")

""" This function is used to create the number of users with number of users as argument"""
# create_user(15000)

""" This function is used to create the groups with number of groups as argument"""
# create_group(300)

""" This function is used to add the user to the group and here number 
    of users are equally distributed in each group"""

# add_user_group()

""" This function is used to add posts and comments"""

# add_post_comment()

