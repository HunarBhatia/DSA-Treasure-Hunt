from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    roll_no = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)