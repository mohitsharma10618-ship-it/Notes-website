from django.urls import path
from . import views

urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('upload/', views.upload_note, name='upload_note'),
    path('my/', views.my_notes, name='my_notes'),
    path('user/<str:username>/', views.user_notes, name='user_notes'),
    path('edit/<int:pk>/', views.edit_note, name='edit_note'),
    path('delete/<int:pk>/', views.delete_note, name='delete_note'),
    path('view/<int:note_id>/', views.view_note, name='view_note'),
    path('download/<int:note_id>/', views.download_note, name='download_note'),
    path('analytics/', views.analytics, name='notes-analytics'),
    path('events/', views.events_list, name='events_list'),
]