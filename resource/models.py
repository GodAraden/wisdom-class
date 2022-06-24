from django.db import models
from user.models import User
from classes.models import Class

class Resource(models.Model):
    description = models.TextField(default='')
    uploader = models.ForeignKey(User,on_delete=models.CASCADE,default=None,null=True)
    classes = models.ForeignKey(Class,on_delete=models.CASCADE,default=None,null=True)
    file = models.FileField(upload_to='')
