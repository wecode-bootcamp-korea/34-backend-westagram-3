from django.db import models

# Create your models here.

class Posting(models.Model):   
    user          = models.ForeignKey('users.User', on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    img_url       = models.URLField()
    post          = models.TextField()
    
    
    class Meta:
        db_table='postings'

class Comment(models.Model):
    post          = models.ForeignKey('Posting', on_delete=models.CASCADE)
    user          = models.ForeignKey('users.User', on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    comment       = models.CharField(max_length=500)
    
    class Meta:
        db_table='comments'
        
class Like(models.Model):
    post          = models.ForeignKey('Posting', on_delete=models.CASCADE)
    user          = models.ForeignKey('users.User', on_delete=models.CASCADE)
    
    
    class Meta:
        db_table='likes'
        
