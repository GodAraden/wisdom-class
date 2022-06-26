import json
from django.http import JsonResponse
from classes.models import Class
from user.models import User
from .models import Notice
from django.core.paginator import Paginator

def getNoticeByClass(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cla = Class.objects.get(id=data.get('class_id'))
        notices = Notice.objects.filter(located_class=cla).order_by('-last_changed')
        arr = []
        if not notices:
            return JsonResponse({'Code':0,'data':{"data":arr,"count":0}})
        paginator = Paginator(notices, 10)
        for k in paginator.page(data.get('currentPage')):
            arr.append({"key":k.id,"creator_id":k.creator.username,"creator":k.creator.name,"title":k.title,"content":k.content,"last_changed":k.last_changed})
        return JsonResponse({'Code':0,'data':{"data":arr,"count":paginator.count}})

def createNotice(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.get(username=data.get('creator'))
        cla = Class.objects.get(id=data.get('class_id'))
        Notice.objects.create(creator=user,located_class=cla,title=data.get('title'),content=data.get('content'))
        return JsonResponse({'Code':0,'data':'发布成功'})

def changeNotice(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.get(username=data.get('user'))
        notice = Notice.objects.get(id=data.get('id'))
        if user != notice.creator:
            return JsonResponse({'Code': 1, 'data': '您不是此条通知的发布者，没有权限修改'})
        notice.title = data.get('title')
        notice.content = data.get('content')
        notice.save()
        return JsonResponse({'Code':0,'data':'修改成功'})

def deleteNotice(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        for id in data.get('ids'):
            notice = Notice.objects.filter(id=id)
            if notice:
                notice[0].delete()
        return JsonResponse({'Code': 0, 'data': '删除成功'})