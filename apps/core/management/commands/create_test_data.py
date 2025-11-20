"""
Django management command to create test users and tasks for development/testing.
Usage: python manage.py create_test_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.core.models import Task
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Create test users and tasks for development and testing purposes'

    def handle(self, *args, **options):
        self.stdout.write('Creating test data...\n')

        # Create test users
        users = []
        user_data = [
            {
                'username': 'alice',
                'email': 'alice@example.com',
                'first_name': 'Alice',
                'last_name': 'Anderson',
                'password': 'TestPassword123!'
            },
            {
                'username': 'bob',
                'email': 'bob@example.com',
                'first_name': 'Bob',
                'last_name': 'Brown',
                'password': 'TestPassword123!'
            },
            {
                'username': 'charlie',
                'email': 'charlie@example.com',
                'first_name': 'Charlie',
                'last_name': 'Clark',
                'password': 'TestPassword123!'
            },
        ]

        for user_info in user_data:
            username = user_info['username']
            if User.objects.filter(username=username).exists():
                self.stdout.write(f'  ⏭️  User "{username}" already exists, skipping...')
                users.append(User.objects.get(username=username))
            else:
                user = User.objects.create_user(
                    username=username,
                    email=user_info['email'],
                    password=user_info['password'],
                    first_name=user_info['first_name'],
                    last_name=user_info['last_name'],
                    is_staff=True,
                )
                users.append(user)
                self.stdout.write(f'  ✅ Created user: {username}')

        self.stdout.write('\n')

        # Create test tasks
        today = datetime.now().date()
        task_data = [
            # Alice's tasks
            {
                'owner': users[0],
                'title': 'Complete project documentation',
                'description': 'Write comprehensive documentation for the security testing project.',
                'status': 'in_progress',
                'priority': 4,
                'due_date': today + timedelta(days=3),
            },
            {
                'owner': users[0],
                'title': 'Review vulnerability report',
                'description': 'Go through the OWASP Top 10 vulnerabilities report and validate findings.',
                'status': 'to_do',
                'priority': 5,
                'due_date': today + timedelta(days=1),
            },
            {
                'owner': users[0],
                'title': 'Setup CI/CD pipeline',
                'description': 'Configure automated testing and deployment pipeline.',
                'status': 'done',
                'priority': 3,
                'due_date': today - timedelta(days=2),
            },
            # Bob's tasks
            {
                'owner': users[1],
                'title': 'Fix broken authentication',
                'description': 'Implement secure session handling and authentication checks.',
                'status': 'in_progress',
                'priority': 5,
                'due_date': today + timedelta(days=2),
            },
            {
                'owner': users[1],
                'title': 'Database optimization',
                'description': 'Optimize slow queries and add proper indexing.',
                'status': 'to_do',
                'priority': 3,
                'due_date': today + timedelta(days=7),
            },
            {
                'owner': users[1],
                'title': 'Code review',
                'description': 'Review pull requests from team members.',
                'status': 'done',
                'priority': 2,
                'due_date': today - timedelta(days=1),
            },
            # Charlie's tasks
            {
                'owner': users[2],
                'title': 'Security audit',
                'description': 'Conduct comprehensive security audit of the application.',
                'status': 'to_do',
                'priority': 5,
                'due_date': today + timedelta(days=5),
            },
            {
                'owner': users[2],
                'title': 'Write unit tests',
                'description': 'Write unit tests to improve code coverage.',
                'status': 'in_progress',
                'priority': 3,
                'due_date': today + timedelta(days=4),
            },
            {
                'owner': users[2],
                'title': 'Deploy to staging',
                'description': 'Deploy the latest version to the staging environment.',
                'status': 'to_do',
                'priority': 4,
                'due_date': today + timedelta(days=2),
            },
            # Shared task (could be visible to all in vulnerable mode)
            {
                'owner': users[0],
                'title': 'Team meeting - Security Discussion',
                'description': 'Discuss security vulnerabilities and best practices with the team.',
                'status': 'to_do',
                'priority': 2,
                'due_date': today + timedelta(days=1),
            },
        ]

        for task_info in task_data:
            # Check if task already exists (by title and owner combination)
            if Task.objects.filter(
                title=task_info['title'],
                owner=task_info['owner']
            ).exists():
                self.stdout.write(f'  ⏭️  Task "{task_info["title"]}" for {task_info["owner"].username} already exists, skipping...')
            else:
                task = Task.objects.create(**task_info)
                self.stdout.write(f'  ✅ Created task: {task.title} (owner: {task.owner.username})')

        self.stdout.write('\n')
        self.stdout.write(self.style.SUCCESS('✨ Test data creation completed!'))
        self.stdout.write('\nTest Users:')
        for user_info in user_data:
            self.stdout.write(f'  - Username: {user_info["username"]}, Password: {user_info["password"]}')
        self.stdout.write('\nYou can now login with any of these credentials.')
