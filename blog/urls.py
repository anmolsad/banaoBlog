from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path("",views.bloghome,name="bloghome"),
    path("create/",views.createblog,name="createblog"),
    path("category/<str:category>/",views.postcategory,name="categorywise"),
    path("blog/<int:id>/",views.blogdetails,name="blogdetails"),
    path("draft/",views.blogdraft,name="blogdraft"),
    path("draft/<int:id>/",views.removedraft,name="removedraft"),
    
]