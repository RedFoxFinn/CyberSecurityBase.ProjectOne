from django.shortcuts import render
from django.views import generic

base_variables = {
    'appname': 'TaskLister',
    'disclaimer': ['This is a programming project for a cyber security course.',
                   'The application is not intended for any serious use and should not be considered to be used as-is.',
                   'Please consider following any proper tutorial instead of using the code of this application as a template.'],
    'appdescription': ['TaskLister is a simple application that allows you to manage your tasks. It is built using Django and can be setup for any user.',
                       'Advanced features makes it secure and only the user can access their own tasks.'],
    'repourl': 'https://github.com/RedFoxFinn/CSBP1'
}
navigation_variables = [
    {'name': 'Home', 'link': '/'},
    {'name': 'Tasks', 'link': '/tasks/'},
    {'name': 'Login', 'link': '/login/'},
    {'name': 'Register', 'link': '/register/'}
]

dummy_tasks = [
    'Task 1: Complete the project documentation',
    'Task 2: Review the code for security vulnerabilities',
    'Task 3: Prepare for the presentation',
    'Task 4: Test the application thoroughly',
    'Task 5: Deploy the application to production'
]

def get_session_value(request, field):
    return request.session.get(field, None)

def set_session_value(request, field, value):
    request.session[field] = value

def delete_session_value(request, field):
    del request.session[field]

def build_context(request):
    context = base_variables.copy()
    context['navigation'] = navigation_variables
    context['request'] = request
    return context

# Create your views here.
def home(request):
    context = build_context(request)
    context['viewname'] = 'Home'
    return render(request, 'home.html', context)

class TaskListView(generic.ListView):
    model = Task

def tasks(request):
    context = build_context(request)
    context['viewname'] = 'Tasks'
    context['tasks'] = dummy_tasks
    return render(request, 'tasks.html', context)

def login(request):
    context = build_context(request)
    context['viewname'] = 'Login'
    return render(request, 'login.html', context)

def register(request):
    context = build_context(request)
    context['viewname'] = 'Register'
    return render(request, 'register.html', context)
