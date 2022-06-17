from django.db import models

# Create your models here.
class User(models.Model):   
    nick_name       = models.CharField(max_length=45,unique=True)
    first_name      = models.CharField(max_length=45)
    last_name       = models.CharField(max_length=45)
    email           = models.CharField(max_length=300,unique=True)
    phone_number    = models.CharField(max_length=20)
    password        = models.CharField(max_length=100)
    
    class Meta:
        db_table='users'

class Follow(models.Model):
    following = models.ForeignKey('User', on_delete=models.CASCADE,related_name='following')
    follower  = models.ForeignKey('User', on_delete=models.CASCADE,related_name='follower')
    
    class Meta:
        db_table='follows'