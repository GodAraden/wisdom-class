from django.urls import path
from . import views
urlpatterns = [
    path('upload',views.upload_view),
    path('update', views.update_view),
    path('delete', views.delete_view),
    path('get', views.all_view),
    path('download',views.download_view)
]
