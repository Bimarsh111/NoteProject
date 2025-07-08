from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login , logout
from noteapp.models import Note
from django.http import JsonResponse
from django.utils import timezone
from noteapp.models import Note
from django.views.decorators.http import require_http_methods
from django.contrib import messages

# Create your views here.

def register_view(request):
    if request.method == 'POST':
       form = UserCreationForm(request.POST)
       if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        initial_data = {'username':'','password1':'','password2':''}
        form = UserCreationForm(initial=initial_data)
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        initial_data = {'username': ''}
        form = AuthenticationForm(initial=initial_data)
    return render(request, 'auth/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def dashboard_view(request):
    query = request.GET.get('q')

    if request.user.is_authenticated:
        user_notes = Note.objects.filter(owner=request.user)
    else:
        user_notes = []

    global_notes = Note.objects.filter(is_public=True)

    if query:
        global_notes = global_notes.filter(title__icontains=query)
        if request.user.is_authenticated:
            user_notes = user_notes.filter(title__icontains=query)

    context = {
        'user_notes': user_notes,
        'global_notes': global_notes,
    }
    return render(request, 'dashboard.html', context)

@login_required
def create_note(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        is_public = request.POST.get('is_public') == '1'
        
        if not content:
            return render(request, 'create_note.html', {
                'error': 'Content is required',
                'title': title,
                'is_public': is_public,
                'content': content
            })
        
        try:
            note = Note.objects.create(
                title=title,
                content=content,
                is_public=is_public,
                owner=request.user
            )
            messages.success(request, 'Note created successfully!')
            return redirect('dashboard')
        except Exception as e:
            return render(request, 'create_note.html', {
                'error': f'Error creating note: {str(e)}',
                'title': title,
                'is_public': is_public,
                'content': content
            })
    
    return render(request, 'create_note.html')

@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, owner=request.user)
    
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        is_public = request.POST.get('is_public') == '1'  # Proper boolean conversion
        
        # Validate both title and content
        if not content or not title:
            error_msg = 'Content is required' if not content else 'Title is required'
            return render(request, 'edit_note.html', {
                'error': error_msg,
                'note': note,
                'title': title,
                'content': content,
                'is_public': is_public
            })
        
        try:
            note.title = title
            note.content = content
            note.is_public = is_public
            note.save()
            
            messages.success(request, 'Note updated successfully!')
            return redirect(f"{reverse('dashboard')}?show_personal=1")
            
        except Exception as e:
            return render(request, 'edit_note.html', {
                'error': f'Error updating note: {str(e)}',
                'note': note,
                'title': title,
                'content': content,
                'is_public': is_public
            })
    
    return render(request, 'edit_note.html', {
        'note': note,
        'title': note.title,
        'content': note.content,
        'is_public': note.is_public
    })

@login_required
def delete_note(request, note_id):
    if request.method == 'POST':
        note = Note.objects.get(id=note_id, owner=request.user)
        note.delete()
        messages.success(request, 'Note deleted successfully!')
        return redirect('dashboard')
    return redirect('dashboard')