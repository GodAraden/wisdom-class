from django.db import models
from user.models import User
from classes.models import Class

class Notice(models.Model):
    located_class = models.ForeignKey(Class,on_delete=models.CASCADE,related_name='located_class',null=True)
    creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name='creator',null=True)
    title = models.CharField(max_length=120,default='')
    content = models.TextField(default='')
    last_changed = models.DateTimeField(auto_now=True)