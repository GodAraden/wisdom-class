import json
from django.http import JsonResponse, FileResponse
from django.utils.encoding import escape_uri_path

from user.models import User
from classes.models import Class
from .models import Resource
from django.core.paginator import Paginator

def upload_view(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        file_id = Resource.objects.create(file=file).id
        return JsonResponse({"Code":0,"data":file_id})

def update_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        description = data.get('description')
        user = User.objects.get(username=data.get('username'))
        cla = Class.objects.get(id=data.get("class_id"))
        try:
            res = Resource.objects.get(id=data.get("file_id"))
            res.uploader = user
            res.classes = cla
            res.description = description
            res.save()
            return JsonResponse({"Code":0,"data":'上传成功'})
        except:
            return JsonResponse({"Code":1,"error":'请上传或重新上传资源'})

def delete_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        res = Resource.objects.get(id=data.get("file_id"))
        try:
            res.delete()
        except:
            return JsonResponse({"Code": 1, "data": '删除失败'})
        return JsonResponse({"Code":0,"data":'删除成功'})

def all_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cla = Class.objects.get(id=data.get('class_id'))
        class_res = Resource.objects.filter(classes=cla).order_by('-id')
        arr = []
        if not class_res:
            return JsonResponse({'Code':0,'data':{"data":arr,"count":0}})
        paginator = Paginator(class_res, 8)
        for k in paginator.page(data.get('currentPage')):
            arr.append({"file_id":k.id,"name":k.file.name,"path":k.file.path,"description":k.description,"uploader":k.uploader.name or '匿名用户',"uploader_id":k.uploader.username,"size":k.file.size})
        return JsonResponse({"Code": 0, "data": {"data":arr,"count":paginator.count}})

def download_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        f = Resource.objects.get(id=data.get("file_id")).file
        file = open(f.path, 'rb')
        print(f.path)
        response = FileResponse(file,filename=f.name, as_attachment=True)
        response['Content-Type']='application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename=utf-8{}'.format(escape_uri_path(f.name))
        return response
