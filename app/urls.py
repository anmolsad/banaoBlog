from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path("",views.home,name="homepage"),
    path("register/",views.register,name="register"),
    path("login/",views.loginpage,name="login"),
    path("dashboard/",views.home,name="homepage"),
    path("logout/",views.logoutview,name="logout")
    
]