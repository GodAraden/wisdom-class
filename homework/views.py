import json
from .models import Homework,Answer
from django.http import JsonResponse
from classes.models import Class
from user.models import User

def createHomework_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cla = Class.objects.get(id=data.get("classID"))
        creator = User.objects.get(username=data.get("creator"))
        Homework.objects.create(classes=cla,creator=creator,title=data.get('title'),content=json.dumps(data.get("questionnaire")))
        return JsonResponse({"Code": 0, 'data': '发布成功'})

def getHomeworkByClass_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cla = Class.objects.get(id=data.get("classID"))
        all = Homework.objects.filter(classes=cla)
        arr = []
        for k in all:
            obj = {"id":k.id,"creator":k.creator.name or '匿名用户',"title":k.title}
            if data.get('username'):
                user = User.objects.get(username=data.get('username'))
                answer = Answer.objects.filter(homework=k,user=user)
                if answer:
                    obj['answered'] = True
                    obj['score'] = answer[0].score
            arr.append(obj)
        return JsonResponse({"Code": 0, 'data': arr})

def getHomeworkById_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        h = Homework.objects.get(id=data.get("id"))
        return JsonResponse({"Code": 0, "data": {"title": h.title, "content": h.content}})

def answer_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        homework = Homework.objects.get(id=data.get("id"))
        user = User.objects.get(username=data.get("username"))
        content = json.dumps(data.get("answer"))
        Answer.objects.create(homework=homework,user=user,content=content)
        return  JsonResponse({"Code": 0, "data": '提交成功'})