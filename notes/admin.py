from django.contrib import admin
from .models import Note, Event

admin.site.register(Note)
admin.site.register(Event)  # Registering the Event model