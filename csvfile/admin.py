from django.contrib import admin
from .models import Profile, Operation, File, FileData
# Register your models here.
admin.site.register(Profile)
admin.site.register(Operation)
admin.site.register(File)
admin.site.register(FileData)