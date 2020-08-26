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

[Untitled](https://www.notion.so/1a3f1f064e66467885fef6100f64a4a0)

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