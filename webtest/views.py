from django.http import JsonResponse,HttpResponse, FileResponse
from resource.models import Resource

def ping_view(request):
    if request.method == 'POST':
        r  =  Resource.objects.get(id=19)
        response = FileResponse(r.file)
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + r.file.name
        return response