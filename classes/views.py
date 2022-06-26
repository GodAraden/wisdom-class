import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from user.models import User
from .models import Class,Class_Members,Class_Request

def create_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.get(username=data.get('creator'))
        c = Class.objects.create(name=data.get('name'),creator_id=user)
        Class_Members.objects.create(class_id=c,member_id=user)
        return JsonResponse({'Code':0,"data":'班级：%s 创建成功！'%(data.get('name'))})

def userClasses_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.get(username=data.get('user'))
        arr = []
        for k in user.class_members_set.all():
            arr.append({'id':k.class_id.id,'name':k.class_id.name})
        return JsonResponse({"Code":0,"data":arr})

def classMember_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        c = Class.objects.get(id=data.get('class_id'))
        arr = []
        paginator = Paginator(c.class_members_set.all(), 10)
        for k in paginator.page(data.get('currentPage')):
            arr.append({'id':k.member_id.id,'name':k.member_id.name or '匿名用户','phone':k.member_id.username,'user_type':k.member_id.user_type})
        return JsonResponse({"Code":0,"data":{"data":arr,"count":paginator.count}})

def searchByPhone_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        users = User.objects.filter(username__contains=data.get('phone'))
        now_members = Class_Members.objects.filter(class_id=data.get('class_id')).values('member_id')
        members_id_set = []
        for k in now_members:
            members_id_set.append(k.get('member_id'))
        arr = [ ]
        for k in users:
            # 查找这个user有没有请求/受邀对应班级的记录
            t = {"id":k.id,"phone":k.username,"name":k.name or '匿名用户',"user_type":k.user_type,'status':255}
            if Class_Request.objects.filter(class_id=data.get('class_id'),request_id=k.id):
                t['status']=Class_Request.objects.filter(class_id=data.get('class_id'),request_id=k.id)[0].status
            arr.append(t)
            classes = k.class_members_set.all()
            for c in classes:
                if t in arr and c.member_id.id in members_id_set:
                    arr.remove(t)
                    break
        if len(arr) == 0:
            return JsonResponse({"Code":1,"error":'暂无匹配项'})
        else:
            return JsonResponse({"Code":0,"data":arr})

def searchClassByName_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        classes = Class.objects.filter(name__contains=data.get('name'))
        arr = []
        for k in classes:
            # -1已发送邀请，0已发送加入请求，1已接受请求，2已拒绝请求，255未发送请求
            t = {'id':k.id,'name':k.name,'creator':k.creator_id.name,'creator_phone':k.creator_id.username,'status':255}
            u = User.objects.get(username=data.get('username'))
            if Class_Members.objects.filter(member_id=u.id,class_id=k.id):
                t['status'] = 1
            elif Class_Request.objects.filter(request_id=u.id,class_id=k.id):
                t['status'] = Class_Request.objects.filter(request_id=u.id,class_id=k.id)[0].status
            arr.append(t)
        if len(arr) == 0:
            return JsonResponse({"Code":1,"error":'暂无匹配项'})
        else:
            return JsonResponse({"Code":0,"data":arr})

def createClassRequest_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        c = Class.objects.get(id=data.get('class_id'))
        req = User.objects.get(username=data.get('username'))
        res = User.objects.get(username=data.get('creator'))
        method = data.get('method')
        if not Class_Request.objects.filter(class_id=c,request_id=req,response_id=res):
            Class_Request.objects.create(class_id=c,request_id=req,response_id=res,status=method)
            return JsonResponse({"Code":0,"data":'发送成功'})
        else:
            return JsonResponse({"Code":1,"error":'请求已经发送过了'})

def getRequests_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.get(username=data.get('username'))
        arr = []
        reqs = []
        if data.get('type') == 0:
            reqs = Class_Request.objects.filter(response_id=user)
        elif data.get('type') == -1:
            reqs = Class_Request.objects.filter(request_id=user)
        for k in reqs:
            if k.status == data.get('type'):
                arr.append({'name':k.request_id.name,'username':k.request_id.username,'class':k.class_id.name,'class_id':k.class_id.id,'status':k.status})
        return JsonResponse({"Code":0,"data":arr})

def manageRequest_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if data.get('status') <= 0:
            return JsonResponse({"Code":1,"data":'无权限操作'})
        c = Class.objects.get(id=data.get('class_id'))
        u = User.objects.get(username=data.get('request'))
        req = Class_Request.objects.get(class_id=c, request_id=u)
        if data.get('status') == 1:
            Class_Members.objects.create(class_id=c, member_id=u)
            str = '添加成功'
        elif data.get('status') == 2:
            str = '拒绝成功'
        req.status = data.get('status')
        req.save()
        return JsonResponse({"Code":0,"data":str})
