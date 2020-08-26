from django.shortcuts import render
from django.http import JsonResponse
import csv, io
from django.db import transaction
from .models import *
import time
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from background_task import background
from datetime import datetime
from django.utils import timezone
from background_task.models import Task
import os
import subprocess
def kill_task(op_id):
    """
    Utility function to stop the background task.

    """


    now = timezone.now()
    running_tasks = Task.objects.filter(verbose_name=str(op_id))
    for i in running_tasks:
        print(i)

    
    try:
        t = Task.objects.get(verbose_name=str(op_id))
        if t.locked_by:
            os.kill(int(t.locked_by),9)
            os.system('cd ..')
            c = subprocess.Popen(['python','manage.py','process_tasks'])
        t.delete()
    except:
        return False
    return True


def register(request):
    """

    Method to register an Operation

    """
    op = Operation()
    op.op_type = request.POST.get('op_type','Default')
    op.save()
    response = {"id":op.id}

    return JsonResponse(response)


def get_status(request):
    """
    Method to get the status of the current upload.

    """
    try:
        op = Operation.objects.get(id=request.POST.get('op_id',None))
    except Exception as e:
        print(e)
        return JsonResponse({"message":"ID Invalid"})
    return JsonResponse({"lines_finished":op.lines_finished,"is_finished":not(op.is_active or op.is_paused or op.is_terminated)})



@background(queue='my-queue')
def file_upload(data_set,op_id,f_id,lines):
    """
    Background task which handles the file upload.

    """
    c=0
    io_string = io.StringIO(data_set)
    next(io_string)
    try:
        op = Operation.objects.get(id=op_id)
        f = File.objects.get(id=f_id)
    except:
        return
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        if c <= int(lines):
            c+=1
            continue
        if op.is_terminated:
            try:
                FileData.objects.get(file=f).delete()
                return
            except:
                return
        op = Operation.objects.get(id=op_id)

        if op.is_paused:
            return 
        elif op.is_active:
            _ = FileData()
            _.name=column[0]
            _.number=column[1]
            _.file=f
            _.save()
            op.lines_finished +=1
            op.save()
    op.is_active=False
    op.is_paused=False
    op.is_terminated=False
    op.save()
    return JsonResponse({"message":"upload successful"})
    


def upload(request):
    """

    Method to both start and resume an upload
    Body:
    {
        "op_id":x,
        "file":xyz.csv,
        "lines":10(Optional)
    }

    Whenever the lines parameter is above 0 it considers the request as a pause

    Response:
    On successful start/resume - {"message":"Upload started"}
    If operation already terminated  - {"message":"Upload already terminated"}
    If op_id invalid - {"message":"Operation ID Invalid"}

    """

    if request.method == "POST":
        try:
            op = Operation.objects.get(id = request.POST.get('op_id',None))
        except e:
            print(e)
            res = {"message":"Operation ID Invalid"}
            return JsonResponse(res)
        f = File()
        f.op = op
        f.save()
        lines = request.POST.get('lines',0)
        if op.is_terminated:
            return JsonResponse({"message":"Process already terminated"})
        if int(lines)>0:
            op.is_paused=False
            op.is_active=True
            op.save()
        csv_file = request.FILES['file']
        
        data_set = csv_file.read().decode('UTF-8')
        file_upload(data_set,op.id,f.id,lines,verbose_name="{}".format(str(op.id)))
        return JsonResponse({"message":"Upload Started"})

def pause(request):
    """

    Method to pause a long running task

    Request Body:
    {
        "op_id":x
    }

    Response:
    On successful Pause - {"success":True}
    If operation already paused  - {"message":"Upload already paused"}
    If op_id invalid - {"message":"Operation ID Invalid"}


    """
    try:
        op = Operation.objects.get(id = request.POST.get('op_id',None))
    except Exception as e:
        print(e)
        res = {"message":"Operation ID Invalid"}
        return JsonResponse(res)
    print(op)
    op.is_paused = True
    op.is_active = False
    op.is_terminated = False
    op.save()
    if kill_task(op.id):
        return JsonResponse({"success":True})
    return JsonResponse({"message":"Upload already paused"})



def terminate(request):
    """

    Message to terminate a paused Operation.

    Body:
    {
        "op_id":True
    }

    Responses:
    If op_id is invalid : {"message":"Operation ID Invalid"}
    If operation is not paused : {"message":"Pause the operation"}
    On successful termination : {"success":True}

    """
    try:
        op = Operation.objects.get(id = request.POST.get('op_id',None))
    except:
        res = {"message":"Operation ID Invalid"}
        return JsonResponse(res)
    if not op.is_paused:
        return JsonResponse({"message":"Pause the operation"})
    op.is_active = False
    op.is_paused = False
    op.is_terminated = True
    op.save()
    f = File.objects.get(op=op)
    
    try:
        FileData.objects.filter(file=f).delete()
    except Exception as e:
        print(e)
        pass
    return JsonResponse({"success":True})

