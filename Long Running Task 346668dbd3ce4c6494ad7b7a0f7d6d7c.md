# Long Running Task

An implementation through which the user can now stop the long-running task at any given point in time, and can choose to resume or terminate it. This will ensure that the resources like compute/memory/storage/time are used efficiently at our end, and do not go into processing tasks that have already been stopped (and then to roll back the work done post the stop-action)

Implemented using `django-background-tasks`. Currently using it on a single thread and processing one task at a time, but the the number of threads can be increased and the job can be done asynchronously too.

## Flow:

- Register an Operation
- Start the Operation
- Pause the Operation
    - Resume the Operation OR
    - Terminat the Operation

## Endpoints

| Endpoints    	| Type 	| Body                                 	| Response                                 	| Remarks                                                                                                                 	|
|--------------	|------	|--------------------------------------	|------------------------------------------	|-------------------------------------------------------------------------------------------------------------------------	|
| /register/   	| POST 	| op_type:"Upload"                     	| op_id: 1                                 	|                                                                                                                         	|
| /upload/     	| POST 	| op_id: 1, file: sample.csv, lines: 5 	| message: upload started                  	| To resume an operation send current lines_finished                                                                      	|
| /pause/      	| POST 	| op_id : 1                            	| success: True                            	| If operation already paused - {"message":"Upload already paused"} If op_id invalid - {"message":"Operation ID Invalid"} 	|
| /terminate/  	| POST 	| op_id : 1                            	| success: True                            	| If op_id is invalid : {"message":"Operation ID Invalid"} If operation is not paused : {"message":"Pause the operation"} 	|
| /get_status/ 	| POST 	| op_id : 1                            	| lines_finished: 100, is_finished : False 	| is_finished : True if the upload is completed                                                                           	|
### Instructions to setup on local host

```
# clone the repository to your local machine
$ git clone https://github.com/Goutham8449/Long-running-task.git

# navigate to the project's directory and install all the relevant dev-dependencies
$ cd long_task && pip install -r requirements.txt

# make migrations
$ python manage.py migrate
$ python manage.py makemigrations

# Start application
$ python manage.py runserver

#In a new terminal
$ python manage.py process_tasks

#Can create a super user to login to django-admin dashboard on http://127.0.0.1:8000/admin
$ python manage.py createsuperuser
$Enter your credentials.
```
