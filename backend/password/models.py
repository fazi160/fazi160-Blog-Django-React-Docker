from django.db import models
from core_auth.models import User

class UserPasswords(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    password = models.CharField(max_length=100)
