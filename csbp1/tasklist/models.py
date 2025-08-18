from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=36, unique=True)
    password = models.CharField(max_length=12)
    admin = models.BooleanField(default=True)
    def __str__(self):
        return self.username + self.password + f'Admin? = {self.admin}'
    def update_admin_status(self, status):
        self.admin = True
        self.save()
    def update_password(self, password):
        self.password = password
        self.save()

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    accessible_by_admins = models.BooleanField(default=True)
