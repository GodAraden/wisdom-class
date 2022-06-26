import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Subject,Score
from classes.models import Class

def subject_view(request):
    if (request.method=='POST'):
        data = json.loads(request.body)
        if not data.get("id"):
            cla = Class.objects.get(id=data.get("class_id"))
            Subject.objects.create(name=data.get('name'),date=data.get("date"),classes=cla)
            return JsonResponse({"Code": 0, "data": "创建成功"})
        else:
            subject = Subject.objects.get(id=data.get("id"))
            subject.name = data.get('name')
            subject.date = date=data.get("date")
            subject.save()
            return JsonResponse({"Code":0,"data":"修改成功"})

def delSubject_view(request):
    if (request.method=='POST'):
        data = json.loads(request.body)
        subject = Subject.objects.get(id=data.get("id"))
        subject.delete()
        return JsonResponse({"Code":0,"data":"删除成功"})

def allSubject_view(request):
    if (request.method=='POST'):
        data = json.loads(request.body)
        cla = Class.objects.get(id=data.get('class_id'))
        subjects = Subject.objects.filter(classes=cla)
        arr = []
        if not subjects:
            return JsonResponse({'Code':0,'data':{"data":arr,"count":0}})
        paginator = Paginator(subjects, 10)
        for k in paginator.page(data.get('currentPage')):
            arr.append({"id":k.id,"name":k.name,"date":k.date})
        return JsonResponse({'Code':0,'data':{"data":arr,"count":paginator.count}})

def subAndClassName_view(request):
    if (request.method=='POST'):
        data = json.loads(request.body)
        subject = Subject.objects.get(id=data.get("id"))
        return JsonResponse({'Code':0,'data':{"subjectName":subject.name,"className":subject.classes.name}})

def addScore_view(request):
    if (request.method=='POST'):
        data = json.loads(request.body)
        return JsonResponse({'Code': 0, 'data': 1})