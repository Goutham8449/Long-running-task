from django.db import models

# Create your models here.
class Profile(models.Model):
    id = models.AutoField('ID', primary_key=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=150,unique=True)
    updated_at = models.DateTimeField('Updated Date', auto_now=True)
    created_at = models.DateTimeField('Created Date', auto_now_add=True)

    def __str__(self):
        return self.name

class Operation(models.Model):
    id = models.AutoField('ID', primary_key=True)
    op_type = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_paused = models.BooleanField(default=False)
    is_terminated = models.BooleanField(default=False)
    lines_finished = models.IntegerField(default=0)

    updated_at = models.DateTimeField('Updated Date', auto_now=True)
    created_at = models.DateTimeField('Created Date', auto_now_add=True)

    def __str__(self):
        return self.op_type

class File(models.Model):
    id = models.AutoField('ID', primary_key=True)
    op = models.ForeignKey(
        Operation,
        on_delete=models.CASCADE,
        related_name='file_op',
        null=True,
        blank=True
    )
    #lines_uploaded = models.CharField(default=0)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField('Updated Date', auto_now=True)
    created_at = models.DateTimeField('Created Date', auto_now_add=True)

    def __str__(self):
        return "File"

class FileData(models.Model):
    id = models.AutoField('ID',primary_key=True)
    name = models.CharField(max_length=150)
    number = models.CharField(max_length=20)
    file = models.ForeignKey(
        File,
        on_delete=models.CASCADE,
        related_name = 'profile_file',
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField('Updated Date', auto_now=True)
    created_at = models.DateTimeField('Created Date', auto_now_add=True)

    def __str__(self):
        return self.name
