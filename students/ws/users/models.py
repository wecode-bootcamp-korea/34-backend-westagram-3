from django.db import models

class User(models.Model):
    username     = models.CharField(max_length=45, unique=True),
    first_name   = models.CharField(max_length=45),
    last_name    = models.CharField(max_length=45),
    email        = models.EmailField(max_length=200, unique=True),
    password     = models.CharField(max_length=100),
    phone_number = models.CharField(max_length=200, unique=True)
    class Meta:
        db_table = 'users'