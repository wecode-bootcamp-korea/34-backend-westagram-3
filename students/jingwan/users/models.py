from django.db import models

# Create your models here.
class User(models.Model):
    name         = models.CharField(max_length=20)
    email        = models.CharField(max_length=100)
    password     = models.IntegerField()
    phone_number = models.IntegerField()

    class Meta:
        db_table = 'user_informations'