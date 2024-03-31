from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path("",views.home,name="bloghome"),
    path("register/",views.register,name="register"),
    path("login/",views.loginpage,name="login"),
    path("dashboard/",views.home,name="dashboard"),
    path("logout/",views.logoutview,name="logout"),
    path('doctor' , views.doctor , name='doctor'),
    path('confirm' , views.confirm , name='confirm'),
    path('bookform/<int:pk>/' , views.bookform , name='bookform'),
    
]