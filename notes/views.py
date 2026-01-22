import os
from django.http import FileResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Sum
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Note
from .forms import NoteForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db import models
from django.core.files.storage import default_storage
from .models import Event
from accounts.emails import send_email



def note_list(request):
    query = request.GET.get('search', '').strip()       # title/subject search
    course_query = request.GET.get('course', '').strip() # course text box

    notes = Note.objects.all()
    if not notes.exists():
        messages.info(request, 'No notes available. Please upload some notes.')
        return render(request, 'notes/note_list.html', {'notes': notes})
    

    # Filter by title OR subject
    if query:
        notes = notes.filter(
            Q(title__icontains=query) |
            Q(subject__icontains=query)
        )

    # Filter by course if typed
    if course_query:
        notes = notes.filter(course__icontains=course_query)

    return render(request, 'notes/note_list.html', {
        'notes': notes,
        'query': query,
        'course_query': course_query,
    })

@login_required
def upload_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.uploaded_by = request.user
            note.save()
            messages.success(request, 'Note uploaded successfully.')
            # 🔔 EMAIL NOTIFICATION (YAHI ADD KARNA HAI)
            users = User.objects.exclude(email='').values_list('email', flat=True)

            send_email(
                to=list(users),
                subject="📢 New Notes Uploaded!",
                html="""
                    <h3>New Notes Uploaded!</h3>
                    <p>A new note has been uploaded on <b>NotesSetu</b>.</p>
                    <p>Visit the website to check it out.</p>
                """
            )
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/upload.html', {'form': form})

@login_required
def my_notes(request):
    notes = Note.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')
    return render(request, 'notes/user_notes.html', {'notes': notes})

def user_notes(request, username):
    from django.contrib.auth.models import User
    profile_user = get_object_or_404(User, username=username)
    notes = Note.objects.filter(uploaded_by=profile_user).order_by('-uploaded_at')
    return render(request, 'notes/user_notes.html', {'notes': notes, 'profile_user': profile_user})

@login_required
def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk, uploaded_by=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated.')
            return redirect('my_notes')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/edit_note.html', {'form': form, 'note': note})

@login_required
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk, uploaded_by=request.user)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted.')
        return redirect('my_notes')
    return render(request, 'notes/confirm_delete.html', {'note': note})

def view_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    # Build full file URL in Python (not in template)
    file_url = None
    if note.upload:
        file_url = request.build_absolute_uri(note.upload.url)

    return render(request, 'notes/view_note.html', {
        'note': note,
        'file_url': file_url
    })
def download_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if not note.upload:                      # no file attached in DB
        raise Http404("File not attached to this note.")

    # note.upload.name is the path relative to the storage root (e.g., 'notes/my.pdf')
    try:
        f = default_storage.open(note.upload.name, 'rb')
    except FileNotFoundError:
        raise Http404("File not found on server.")

    # increment download count (optional)
    Note.objects.filter(id=note_id).update(download_count=models.F('download_count') + 1)

    filename = os.path.basename(note.upload.name)
    return FileResponse(f, as_attachment=True, filename=filename)

@staff_member_required
def analytics(request):
    total_notes = Note.objects.count()
    total_downloads = Note.objects.aggregate(s=Sum('download_count'))['s'] or 0
    notes_by_user = Note.objects.values('uploaded_by__username').annotate(c=Count('id')).order_by('-c')
    downloads_top = Note.objects.values('title').annotate(d=Sum('download_count')).order_by('-d')[:10]

    return render(request, 'notes/analytics.html', {
        'total_notes': total_notes,
        'total_downloads': total_downloads,
        'notes_by_user': notes_by_user,
        'downloads_top': downloads_top,
    })

def events_list(request):
    events = Event.objects.order_by('-date')
    return render(request, 'notes/events.html', {'events': events})