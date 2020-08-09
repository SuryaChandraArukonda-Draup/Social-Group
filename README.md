# Social-Group
Tech Stack: Python, Flask, Mongodb, and RQ

### Description:

A platform to connect with people and share your thoughts. Let's you create a social group with role based access control.

### Prerequisites:

Python 3.6 or above:

    1. Flask and other Python libraries with latest versions.
    2. Mongodb installed with a local database connection established.
    3. Redis Queue installed with a local connection established.

### Installation:

    1. Clone the repository.
    2. Install all the prerequisite files.
    3. Run the app.py file using a python interpreter.


# List of APIs:

    1. api.add_resource(User1, '/api/user')

        Example for body: { "name":"surya", "password":"chandra", "email":"surya@gmail.com" }

        Note : Once the user is creted, authorisation is needed in all the APIs. Use your username and password in the authorisation tab before submitting the request.
    
    2. api.add_resource(Group1, '/api/group')
    
        body { "name":"group", "visibility":"private" }
    
    3. api.add_resource(AddToGroup1, '/api/group/<group_id>/add')
    
        body { "new_user":{"arin":"MEMBER"} }
    
    4. api.add_resource(RemoveUserGroup1, '/api/group/<group_id>/remove')

        body { "del_user_id":"" }
    
    5. api.add_resource(ReadGroup1, '/api/group/<group_id>/read')
    
        no body needed 
    
    6. api.add_resource(Post1, '/api/group/<group_id>/post/add')
    
        body { "content":"my first post" }
    
    7. api.add_resource(DeletePost1, '/api/group/<group_id>/post/<post_id>/delete')
    
        no body needed
    
    8. api.add_resource(Comment1, '/api/group/<group_id>/post/<post_id>/comment/add')
    
        body { "content":"my first comment" }
    
    9. api.add_resource(DeleteComment1, '/api/group/<group_id>/comment/<comment_id>/delete')

        no body needed
    
    
# Data dump

The data dump can be done by running the functions from the data dump directory. In the module go to the file dump.py and run the function one by one.

    1. So, first make users say 15000.
    2. Then make groups say 300 using create_group function and select users and group such that users % groups == 0. So, for this case 15000/300 gives 50 users in each group.
    3. Then run the create_user to group function which distributes all the users in these group equally.
    4. Finally run the add_post_comment function which makes a post and comment from each user.