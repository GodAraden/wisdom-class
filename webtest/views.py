from django.http import JsonResponse
from user.models import User

def ping_view(request):
    if request.method == 'GET':
        user = User.objects.get(username='17800000000')
        user.set_sex('男')
        user.save()
        res = {"Code":0,"data":User.objects.get(username='17800000000').sex}
        return JsonResponse(res)