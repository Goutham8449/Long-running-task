# Long-running-task

An implementation through which the user can now stop the long-running task at any given point in time, and can choose to resume or terminate it. This will ensure that the resources like compute/memory/storage/time are used efficiently at our end, and do not go into processing tasks that have already been stopped (and then to roll back the work done post the stop-action)

Flow:
--> Register an Operation


--> Start the Operation

--> Pause the Operation

    --> Terminate the Operation (rollback) 

    --> Resume the Opeation
    
    
#Endpoints
1. /register/ 
