from django.urls import path
from . import views
urlpatterns = [
    path('register',views.register_view),
    path('login', views.login_view),
    path('logout', views.logout_view),
    path('whoAmI', views.whoAmI_view),
    path('changeInfo',views.changeInfo_view)
]
