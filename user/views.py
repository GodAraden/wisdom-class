import json
from django.http import JsonResponse
from .models import User,TeacherPhone
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if User.objects.filter(username=data.get('username')):
            return JsonResponse({'Code':1,"error":'该手机号已被注册'})
        if TeacherPhone.objects.filter(phone=data.get('username')):
            User.objects.create_user(username=data.get('username'), password=data.get('password'),user_type=0)
            t_phone = TeacherPhone.objects.get(phone=data.get('username'))
            t_phone.used = True
            t_phone.save()
            res = {"Code": 0, "data": '教师账号注册成功'}
        else:
            User.objects.create_user(username=data.get('username'), password=data.get('password'),user_type=1)
            res = {"Code": 0, "data": '学生账号注册成功'}
        return JsonResponse(res)

def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(username=data.get('username'),password=data.get('password'))
        if not user:
            return JsonResponse({'Code':1,"error":'用户名或密码错误'})
        else:
            login(request, user)
            return JsonResponse({"Code": 0, "data": '登录成功'})

def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return JsonResponse({"Code": 0, "data": '退出成功'})

def whoAmI_view(request):
    if request.method == 'GET':
        try:
            user = request.user
            user = {
                "username":user.get_username(),
                "user_type":user.user_type,
                "email":user.user_email,
                "name":user.name,
                "sex":user.sex,
                "birthday":user.birday,
                "number":user.number
            }
            return JsonResponse({"Code": 0, "data": user})
        except Exception as e:
            print(e)
            return JsonResponse({"Code": 1, "data": 'none'})

def changeInfo_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        user.set_email(data.get('email'))
        user.set_name(data.get('name'))
        user.set_sex(data.get('sex'))
        user.set_birthday(data.get('birthday'))
        user.set_number(data.get('number'))
        user.save()
        return JsonResponse({"Code": 0, "data": '修改成功'})