"""
Views for the core application - Task Management System.

VULNERABILITIES DEMONSTRATED:
A01 - Broken Access Control: Improper authorization checks on task operations
A04 - Insecure Design: Lack of authorization design in the system architecture
A07 - Identification and Authentication Failures: Missing authentication checks
A08 - Software and Data Integrity Failures: Data can be modified by unauthorized users

VULNERABILITY BEHAVIOR:
In VULNERABLE mode:
- All tasks visible to all users (including anonymous/unauthenticated)
- Logged-in users can EDIT/DELETE ANY task (not just their own)
- Only task creators can CREATE tasks (this part is secure)

In SECURE mode:
- Users can only view/edit/delete their own tasks
- Anonymous users cannot view any tasks
- Proper authorization checks on all operations
"""
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.db import connection
from django.views.decorators.csrf import csrf_protect
from apps.core.models import Task
import logging
from html import escape

logger = logging.getLogger(__name__)


def home(request):
    """Home page showing the task management application and vulnerability status."""
    context = {
        'vulnerable_mode': settings.VULNERABLE,
        'mode_status': 'VULNERABLE' if settings.VULNERABLE else 'SECURE',
        'user': request.user,
    }
    return render(request, 'core/landing.html', context)


def task_list_view(request):
    """HTML view for task listing page."""
    if settings.VULNERABLE:
        # VULNERABLE: Show all tasks to everyone
        tasks = Task.objects.all()
    else:
        # SECURE: Only show authenticated users their own tasks
        if not request.user.is_authenticated:
            tasks = []
        else:
            tasks = Task.objects.filter(owner=request.user)

    context = {
        'tasks': tasks,
        'vulnerable_mode': settings.VULNERABLE,
        'mode_status': 'VULNERABLE' if settings.VULNERABLE else 'SECURE',
        'user': request.user,
    }
    return render(request, 'core/tasks.html', context)


def task_detail_view(request, task_id):
    """HTML view for task detail page."""
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return render(request, 'core/404.html', {'message': 'Task not found'}, status=404)

    if settings.VULNERABLE:
        # VULNERABLE: Anyone can view any task
        pass
    else:
        # SECURE: Only owner or admin can view
        if not request.user.is_authenticated or (task.owner != request.user and not request.user.is_staff):
            return render(request, 'core/404.html', {'message': 'Access denied'}, status=403)

    context = {
        'task': task,
        'vulnerable_mode': settings.VULNERABLE,
        'mode_status': 'VULNERABLE' if settings.VULNERABLE else 'SECURE',
        'user': request.user,
    }
    return render(request, 'core/task_detail.html', context)


def task_edit_view(request, task_id):
    """HTML view for task editing page."""
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return render(request, 'core/404.html', {'message': 'Task not found'}, status=404)

    if settings.VULNERABLE:
        # VULNERABLE: Anyone can edit any task (no auth required)
        pass
    else:
        # SECURE: Only owner can edit (requires auth)
        if not request.user.is_authenticated:
            return render(request, 'core/404.html', {'message': 'Authentication required'}, status=401)
        if task.owner != request.user:
            return render(request, 'core/404.html', {'message': 'Access denied'}, status=403)

    if request.method == 'POST':
        task.title = escape(request.POST.get('title', task.title).strip())
        task.description = escape(request.POST.get('description', task.description).strip())
        task.status = request.POST.get('status', task.status)
        task.priority = min(int(request.POST.get('priority', task.priority)), 5)
        task.save()
        return render(request, 'core/task_detail.html', {
            'task': task,
            'message': 'Task updated successfully',
            'vulnerable_mode': settings.VULNERABLE,
            'mode_status': 'VULNERABLE' if settings.VULNERABLE else 'SECURE',
            'user': request.user,
        })

    context = {
        'task': task,
        'vulnerable_mode': settings.VULNERABLE,
        'mode_status': 'VULNERABLE' if settings.VULNERABLE else 'SECURE',
        'user': request.user,
        'statuses': Task.STATUS_CHOICES,
    }
    return render(request, 'core/task_edit.html', context)


def task_create_view(request):
    """HTML view for task creation page."""
    # In both modes, only authenticated users can create tasks for themselves
    if not request.user.is_authenticated:
        return render(request, 'core/404.html', {'message': 'Authentication required to create tasks'}, status=401)

    if request.method == 'POST':
        title = escape(request.POST.get('title', '').strip())
        description = escape(request.POST.get('description', '').strip())
        status = request.POST.get('status', 'to_do')
        priority = min(int(request.POST.get('priority', 3)), 5)
        due_date = request.POST.get('due_date', None)

        if not title:
            # If coming from tasks page, redirect back with error message
            if request.META.get('HTTP_REFERER', '').endswith('/tasks/'):
                return render(request, 'core/tasks.html', {
                    'error': 'Task title is required',
                    'tasks': Task.objects.all() if settings.VULNERABLE else Task.objects.filter(owner=request.user) if request.user.is_authenticated else [],
                    'vulnerable_mode': settings.VULNERABLE,
                    'mode_status': 'VULNERABLE' if settings.VULNERABLE else 'SECURE',
                    'user': request.user,
                })
            else:
                return render(request, 'core/task_create.html', {
                    'error': 'Task title is required',
                    'vulnerable_mode': settings.VULNERABLE,
                    'mode_status': 'VULNERABLE' if settings.VULNERABLE else 'SECURE',
                    'user': request.user,
                })

        # Create task - always owned by current user
        task = Task.objects.create(
            title=title,
            description=description,
            owner=request.user,
            status=status,
            priority=priority,
            due_date=due_date if due_date else None,
        )

        # If coming from tasks page, redirect back to tasks list
        if request.META.get('HTTP_REFERER', '').endswith('/tasks/'):
            return render(request, 'core/task_detail.html', {
                'task': task,
                'message': 'Task created successfully! Redirecting...',
                'vulnerable_mode': settings.VULNERABLE,
                'mode_status': 'VULNERABLE' if settings.VULNERABLE else 'SECURE',
                'user': request.user,
                'redirect_url': '/tasks/',
            })
        else:
            return render(request, 'core/task_detail.html', {
                'task': task,
                'message': 'Task created successfully',
                'vulnerable_mode': settings.VULNERABLE,
                'mode_status': 'VULNERABLE' if settings.VULNERABLE else 'SECURE',
                'user': request.user,
            })

    context = {
        'vulnerable_mode': settings.VULNERABLE,
        'mode_status': 'VULNERABLE' if settings.VULNERABLE else 'SECURE',
        'user': request.user,
        'statuses': Task.STATUS_CHOICES,
    }
    return render(request, 'core/task_create.html', context)


@require_http_methods(["GET"])
def task_list_endpoint(request):
    if settings.VULNERABLE:
        # VULNERABLE CODE: No authorization - all tasks visible to everyone
        tasks = Task.objects.all()
    else:
        # SECURE CODE: Only authenticated users can view tasks
        if not request.user.is_authenticated:
            return JsonResponse(
                {'error': 'Authentication required', 'tasks': []},
                status=401
            )
        # Users only see their own tasks
        tasks = Task.objects.filter(owner=request.user)

    task_data = [
        {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'owner': task.owner.username,
            'status': task.status,
            'priority': task.priority,
            'created_at': task.created_at.isoformat(),
            'updated_at': task.updated_at.isoformat(),
            'due_date': task.due_date.isoformat() if task.due_date else None,
        }
        for task in tasks
    ]

    return JsonResponse({
        'success': True,
        'tasks': task_data,
        'mode': 'VULNERABLE' if settings.VULNERABLE else 'SECURE',
        'authenticated': request.user.is_authenticated,
    })


@require_http_methods(["GET"])
def task_detail_endpoint(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)

    if settings.VULNERABLE:
        # VULNERABLE CODE: No ownership check - anyone can see any task
        pass
    else:
        # SECURE CODE: Verify ownership before returning task
        if not request.user.is_authenticated or task.owner != request.user:
            return JsonResponse({'error': 'Access denied'}, status=403)

    task_data = {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'owner': task.owner.username,
        'owner_id': task.owner.id,
        'status': task.status,
        'priority': task.priority,
        'created_at': task.created_at.isoformat(),
        'updated_at': task.updated_at.isoformat(),
        'due_date': task.due_date.isoformat() if task.due_date else None,
    }

    return JsonResponse({
        'success': True,
        'task': task_data,
        'mode': 'VULNERABLE' if settings.VULNERABLE else 'SECURE',
    })


@require_http_methods(["POST"])
@csrf_protect
def task_create_endpoint(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {'error': 'Authentication required to create tasks'},
            status=401
        )

    import json
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    title = data.get('title', '').strip()
    description = data.get('description', '').strip()

    if not title:
        return JsonResponse({'error': 'Title is required'}, status=400)

    # Create task with current user as owner
    task = Task.objects.create(
        title=escape(title),  # Escape HTML to prevent stored XSS
        description=escape(description),
        owner=request.user,
        priority=min(int(data.get('priority', 1)), 5),
    )

    return JsonResponse({
        'success': True,
        'task_id': task.id,
        'message': 'Task created successfully',
        'mode': 'VULNERABLE' if settings.VULNERABLE else 'SECURE',
    })


@require_http_methods(["PUT", "PATCH"])
@csrf_protect
def task_update_endpoint(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    if settings.VULNERABLE:
        # VULNERABLE CODE: Any authenticated user can edit any task
        pass
    else:
        # SECURE CODE: Only owner can edit the task
        if task.owner != request.user:
            return JsonResponse({'error': 'Access denied - you can only edit your own tasks'}, status=403)

    import json
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    # Update allowed fields
    if 'title' in data:
        task.title = escape(data['title'].strip())
    if 'description' in data:
        task.description = escape(data['description'].strip())
    if 'status' in data and data['status'] in dict(Task.STATUS_CHOICES):
        task.status = data['status']
    if 'priority' in data:
        task.priority = min(int(data['priority']), 5)

    task.save()

    return JsonResponse({
        'success': True,
        'message': 'Task updated successfully',
        'task_id': task.id,
        'mode': 'VULNERABLE' if settings.VULNERABLE else 'SECURE',
    })


@require_http_methods(["DELETE"])
@csrf_protect
def task_delete_endpoint(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    if settings.VULNERABLE:
        # VULNERABLE CODE: Any authenticated user can delete any task
        pass
    else:
        # SECURE CODE: Only owner can delete the task
        if task.owner != request.user:
            return JsonResponse({'error': 'Access denied - you can only delete your own tasks'}, status=403)

    task_id = task.id
    task.delete()

    return JsonResponse({
        'success': True,
        'message': 'Task deleted successfully',
        'deleted_task_id': task_id,
        'mode': 'VULNERABLE' if settings.VULNERABLE else 'SECURE',
    })


@require_http_methods(["GET"])
def search_tasks_endpoint(request):
    """
    Search tasks by title.
    
    VULNERABILITY A03 - Injection (SQL Injection):
    In VULNERABLE mode: Uses raw SQL with unsanitized user input, allowing SQL injection attacks
    In SECURE mode: Uses Django ORM which provides automatic SQL parameterization
    """
    search_query = request.GET.get('q', '').strip()

    if not search_query:
        return JsonResponse({
            'success': False,
            'error': 'Search query required',
            'mode': 'VULNERABLE' if settings.VULNERABLE else 'SECURE',
        })

    if settings.VULNERABLE:
        # VULNERABLE CODE: SQL Injection vulnerability - Direct string interpolation
        # Attacker can inject SQL code through the 'q' parameter
        # Examples:
        #   ?q=' OR '1'='1                              (bypass search)
        #   ?q=' UNION SELECT * FROM auth_user --       (extract user data)
        #   ?q=' AND 1=0 UNION SELECT id,username,username,email,email FROM auth_user -- (dump users)
        try:
            query = f"SELECT * FROM core_task WHERE title LIKE '%{search_query}%'"
            tasks = Task.objects.raw(query)
            task_list = [
                {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'owner': task.owner.username,
                    'status': task.status,
                    'priority': task.priority,
                }
                for task in tasks
            ]
            return JsonResponse({
                'success': True,
                'query': search_query,
                'results': task_list,
                'count': len(task_list),
                'mode': 'VULNERABLE',
            })
        except Exception as e:
            # Return the error message to help attackers understand the SQL syntax
            return JsonResponse({
                'success': False,
                'error': str(e),
                'mode': 'VULNERABLE',
            }, status=400)
    else:
        # SECURE CODE: Uses Django ORM with parameterized queries
        # The ORM automatically escapes all user input
        tasks = Task.objects.filter(title__icontains=search_query)

        task_list = [
            {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'owner': task.owner.username,
                'status': task.status,
                'priority': task.priority,
            }
            for task in tasks
        ]

        return JsonResponse({
            'success': True,
            'query': search_query,
            'results': task_list,
            'count': len(task_list),
            'mode': 'SECURE',
        })


@require_http_methods(["GET"])
def status_endpoint(request):
    """Endpoint showing the current vulnerability status and system info."""
    return JsonResponse({
        'application_name': 'Task Management System - CSB Project 1',
        'application_type': 'Task Management with Permission Vulnerabilities',
        'vulnerable_mode': settings.VULNERABLE,
        'mode': 'VULNERABLE' if settings.VULNERABLE else 'SECURE',
        'authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else 'anonymous',
    })


def logout_view(request):
    """Handle user logout and redirect to home."""
    from django.contrib.auth import logout
    logout(request)
    return redirect('core:home')


def register_view(request):
    """Handle user registration and create superuser by default."""
    from django.contrib.auth.models import User
    from django.contrib import messages

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        password_confirm = request.POST.get('password_confirm', '').strip()

        # Validation
        errors = []

        if not username:
            errors.append('Username is required.')
        elif len(username) < 3:
            errors.append('Username must be at least 3 characters long.')
        elif User.objects.filter(username=username).exists():
            errors.append('Username already exists.')

        if not email:
            errors.append('Email is required.')
        elif User.objects.filter(email=email).exists():
            errors.append('Email already registered.')

        if not password:
            errors.append('Password is required.')
        elif len(password) < 6:
            errors.append('Password must be at least 6 characters long.')
        elif password != password_confirm:
            errors.append('Passwords do not match.')

        if errors:
            return render(request, 'core/register.html', {
                'errors': errors,
                'username': username,
                'email': email,
                'vulnerable_mode': settings.VULNERABLE,
                'mode_status': 'VULNERABLE' if settings.VULNERABLE else 'SECURE',
                'user': request.user,
            })

        # Create superuser
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
        )

        messages.success(request, f'Account created successfully! Welcome {username}. You are now logged in as a superuser.')

        # Auto-login the user
        from django.contrib.auth import authenticate, login
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

        return redirect('core:task_list')

    # GET request - show registration form
    return render(request, 'core/register.html', {
        'vulnerable_mode': settings.VULNERABLE,
        'mode_status': 'VULNERABLE' if settings.VULNERABLE else 'SECURE',
        'user': request.user,
    })


def login_view(request):
    """Custom login view that redirects all users to the site after login."""
    from django.contrib.auth import authenticate, login

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to tasks page for all users (including superusers)
            return redirect('core:task_list')
        else:
            # Invalid credentials - show error
            return render(request, 'core/login.html', {
                'error': 'Invalid username or password',
                'vulnerable_mode': settings.VULNERABLE,
                'mode_status': 'VULNERABLE' if settings.VULNERABLE else 'SECURE',
                'user': request.user,
            })

    # GET request - show login form
    return render(request, 'core/login.html', {
        'vulnerable_mode': settings.VULNERABLE,
        'mode_status': 'VULNERABLE' if settings.VULNERABLE else 'SECURE',
        'user': request.user,
    })
