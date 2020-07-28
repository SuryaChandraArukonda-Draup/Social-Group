# Social-Group

#Work Completed:

1. Formulation of program architecture.
2. done with the app configuration and URL for API requests.		
3. Implemented the document schema.						

Monday's work: implementing authentication and authorization.

/Project #The main app folder

run.py		#gets the application running
app.py		#social group application
/error
	error.py	#file containing the error response
/model
	__init__.py
	models.py		#use data through python objects 
/config
	__init__.py
	config.py 		#this config file makes connection to the database
/view
	__init__.py
	mail.py			
	comment.py		#files containing user services
	post.py
	

/url
	url.py			#assigning the routes
/auth
	auth.py			#assigning authorisation

/taskqueue			#Queued tasks
	feed.py			#functions handles the daily feed for
	inactive.py		#delete the inactive members
	notify.py		#daily notification for posts
/datadump
	__init__.py
	dump.py
  
  
#Mongodb schema

Entities: - Permission * ID * Name

- Role
    * ID
    * NAME
    * Permission[]
- User
    * ID
    * NAME
    * email
    * groups =[]
* posts = []
* comments = []
- GROUP
    * ID
    * Name
    * Users {} with id and role
    * Visibilty = PUBLIC | PRIVATE
- POST
    * ID
    * UserId
    * GroupId
    * approval boolean
    * content

- Comment
    * Id
    * PostId
    * userId
    * content
