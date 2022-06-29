from django.http import JsonResponse,HttpResponse, FileResponse
from resource.models import Resource

def ping_view(request):
    if request.method == 'POST':
        return JsonResponse({"Code":0,'data':'pong'})