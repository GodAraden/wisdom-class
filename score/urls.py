from django.urls import path
from . import views
urlpatterns = [
    path("subject/add",views.subject_view),
    path("subject/update", views.subject_view),
    path("subject/delete",views.delSubject_view),
    path("subject/get",views.allSubject_view),
    path("subject/name", views.subAndClassName_view),
    path('get',views.getScore_view),
    path('sync',views.syncScore_view),
    path('excel',views.excel_view),
    path('analyze',views.analyze_view),
    path('number', views.getScoreByNumber_view),
]
