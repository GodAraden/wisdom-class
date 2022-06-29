import json
import os
import WisdomClass.settings
import xlsxwriter
from django.core.paginator import Paginator
from django.http import JsonResponse, FileResponse
from django.utils.encoding import escape_uri_path
from django.db.models import Sum,Avg,Count,Max,Min
from .models import Subject,Score
from classes.models import Class
from user.models import User

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
        subjects = Subject.objects.filter(classes=cla).order_by("-date")
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

def getScore_view(request):
    if (request.method=='POST'):
        data = json.loads(request.body)
        subject = Subject.objects.get(id=data.get("id"))
        all_score = Score.objects.filter(subject=subject)
        arr = []
        for k in all_score:
            arr.append({"number":k.student_number,"name":k.student_name,"score":k.score})
        return JsonResponse({'Code': 0, 'data': arr })

def syncScore_view(request):
    if (request.method=='POST'):
        data = json.loads(request.body)
        subject = Subject.objects.get(id=data.get('id'))
        scores = Score.objects.filter(subject=subject)
        for k in scores:
            k.delete()
        for k in data.get('data'):
            Score.objects.create(subject=subject,student_name=k.get('name'),student_number=k.get('number'),score=k.get('score'))
        return JsonResponse({'Code': 0, 'data': "同步成功" })

def excel_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        subject = Subject.objects.get(id=data.get("id"))
        filename = "%s_%s.xlsx"%(subject.name,subject.classes.name)
        path = "%s\media\score\%s"%(WisdomClass.settings.BASE_DIR,filename)
        workbook = xlsxwriter.Workbook(path)
        sheet1 = workbook.add_worksheet("sheet1")
        scores = Score.objects.filter(subject=subject)
        for i in range(0,len(scores)):
          sheet1.write(i,0,scores[i].student_number)
          sheet1.write(i,1,scores[i].student_name)
          sheet1.write(i,2,scores[i].score)
        workbook.close()
        file = open(path, 'rb')
        response = FileResponse(file,filename=filename, as_attachment=True)
        response['Content-Type']='application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename=utf-8{}'.format(escape_uri_path(filename))
        return response

def analyze_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        subject = Subject.objects.get(id=data.get("id"))
        scores = Score.objects.filter(subject=subject).order_by('-score')
        if not scores:
            return JsonResponse({"Code":1,"error":"请先导入学生数据"})
        avgScore = round(scores.aggregate(Avg("score")).get('score__avg'),2)
        maxScore = {"score":scores[0].score,"name":scores[0].student_name,"number":scores[0].student_number}
        minScore = {"score":scores[len(scores)-1].score,"name":scores[len(scores)-1].student_name,"number":scores[len(scores)-1].student_number}
        total = [{"name":"挂科","value":len(scores.filter(score__lt=60))},{"name":"通过","value":len(scores.filter(score__gte=60))}]
        subsection = {"xAxis":[],"data":[]}
        interval = data.get('interval')
        current = 0
        while(current < 100):
            range = None
            if (current + interval > 100):
                range = (current,100)
            else:
                range = (current,current+interval)
            subsection['xAxis'].append(str(range))
            subsection['data'].append(len(scores.filter(score__range=range)))
            current += interval
        return JsonResponse({'Code': 0, 'data': {"avg":avgScore,"max":maxScore,"min":minScore,"total":total,"subsection":subsection} })

def getScoreByNumber_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        student = User.objects.get(username=data.get('username'))
        scores = Score.objects.filter(student_number=student.number)
        if not scores:
            return JsonResponse({"Code":1,"error":"没有对应的成绩，请检查学号是否有误或老师未上传成绩"})
        arr = []
        for k in scores:
            arr.append({"name":k.subject.name,"score":k.score})
        return JsonResponse({"Code":0,"data":arr})
