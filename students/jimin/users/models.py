from django.db import models

# Create your models here.
class User(models.Model):   
    first_name      = models.CharField(max_length=45,default='')
    last_name       = models.CharField(max_length=45,default='')
    email           = models.CharField(max_length=300,unique=True)
    phone_number    = models.CharField(max_length=20,default='')
    password        = models.CharField(max_length=45,default='')
    
    class Meta:
        db_table='users'