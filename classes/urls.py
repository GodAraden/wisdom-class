from django.urls import path
from . import views
urlpatterns = [
    path('create',views.create_view),
    path('user',views.userClasses_view),
    path('member', views.classMember_view),
    path('search/member', views.searchByPhone_view),
    path('search/class', views.searchClassByName_view),
    path('request/send', views.createClassRequest_view),
    path('request/get',views.getRequests_view),
    path('request/manage',views.manageRequest_view)
]
