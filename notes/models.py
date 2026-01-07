from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
import os
User = get_user_model()

def protected_upload_path(instance, filename):
    return os.path.join('notes', filename)  # stored under PROTECTED_MEDIA_ROOT/notes

class Note(models.Model):
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    course = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=120, blank=True)
    semester = models.PositiveSmallIntegerField(null=True, blank=True)
    upload = models.FileField(upload_to='notes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="note_list/",null=True, blank=True,default=None)  # for file list

class Event(models.Model):
     title = models.CharField(max_length=200)
     description = models.TextField()
     date = models.DateField()
     created_at = models.DateTimeField(auto_now_add=True)
        
def __str__(self):
    return self.title