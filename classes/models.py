from django.db import models
from user.models import User

class Class(models.Model):
    name = models.CharField(max_length=50,default='')
    creator_id = models.ForeignKey(User,on_delete=models.CASCADE)

class Class_Members(models.Model):
    class_id = models.ForeignKey(Class,on_delete=models.CASCADE)
    member_id = models.ForeignKey(User,on_delete=models.CASCADE)

class Class_Request(models.Model):
    class_id =  models.ForeignKey(Class,on_delete=models.CASCADE,related_name="req_class_id")
    request_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="request_id")
    response_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="response_id")
    # -1已发送邀请，0已发送加入请求，1已接受请求，2已拒绝请求
    status = models.IntegerField(default=0)