from django.db import models
from classes.models import Class
from user.models import User

class Subject(models.Model):
    name = models.CharField(max_length=40,default='')
    date = models.DateField(default='')
    classes = models.ForeignKey(Class,on_delete=models.CASCADE)

# 班级id 学生id 考试时间  科目名称 分数
class Score(models.Model):
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    score = models.FloatField()