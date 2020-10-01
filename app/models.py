from django.db import models
# Create your models here.
class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length = 100,blank = True,default='',null='')

    class Meta:
        ordering = ['created']
