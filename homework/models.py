from django.db import models
from user.models import User
from classes.models import Class

class Homework(models.Model):
    title = models.CharField(max_length=80,default='')
    content = models.TextField(default='')
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    classes = models.ForeignKey(Class,on_delete=models.CASCADE)

class Answer(models.Model):
    homework = models.ForeignKey(Homework,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField(default='')
    score = models.IntegerField(default=None,null=True)