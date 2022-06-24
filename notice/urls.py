from django.urls import path
from . import views
urlpatterns = [
    path('get',views.getNoticeByClass),
    path('create', views.createNotice),
    path('change',views.changeNotice),
    path('delete',views.deleteNotice)
]
