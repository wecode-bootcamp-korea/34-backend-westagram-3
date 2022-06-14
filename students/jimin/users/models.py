from django.db import models

# Create your models here.
class User(models.Model):   
    first_name      = models.CharField(max_length=45)
    last_name       = models.CharField(max_length=45)
    email           = models.CharField(max_length=300,unique=True)
    phone_number    = models.CharField(max_length=20)
    password        = models.CharField(max_length=45)
    
    class Meta:
        db_table='users'
  
        
        