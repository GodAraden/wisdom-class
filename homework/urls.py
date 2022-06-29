from django.urls import path
from . import views
urlpatterns = [
    path('create',views.createHomework_view),
    path('getall', views.getHomeworkByClass_view),
    path("getone",views.getHomeworkById_view),
    path("answer",views.answer_view)
]
