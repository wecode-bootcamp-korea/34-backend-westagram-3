from django.db import models

# Create your models here.
class TimeStampModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    class Mete:
        abstract = True

class Posting(TimeStampModel):   
    user          = models.ForeignKey('users.User', on_delete=models.CASCADE)
    img_url       = models.URLField()
    post          = models.TextField()
    
    class Meta:
        db_table='postings'

class Comment(TimeStampModel):
    post          = models.ForeignKey('Posting', on_delete=models.CASCADE)
    user          = models.ForeignKey('users.User', on_delete=models.CASCADE)
    comment       = models.CharField(max_length=500)
    
    class Meta:
        db_table='comments'
        
class Like(TimeStampModel):
    post          = models.ForeignKey('Posting', on_delete=models.CASCADE)
    user          = models.ForeignKey('users.User', on_delete=models.CASCADE)
    
    class Meta:
        db_table='likes'
        
