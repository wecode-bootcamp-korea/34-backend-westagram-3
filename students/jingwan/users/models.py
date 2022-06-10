from django.db import models

# Create your models here.
class User(models.Model):
    user_name    = models.CharField(max_length=30)
    first_name   = models.CharField(max_length=161)
    last_name    = models.CharField(max_length=11)
    email        = models.CharField(max_length=254, unique=True)
    password     = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'user_informations'