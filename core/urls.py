from django.contrib import admin
from django.urls import path
from . import views
from .views import Register,Logout,Login,Updating,ViewUser
urlpatterns = [
    path('',views.home,name="home"),
    path('register/',Register.as_view(),name="register"),
    path('logout/',Logout.as_view(),name="logout"),
    path('login/',Login.as_view(),name="login"),
    path('updating/',Updating.as_view(),name = "update"),
    path('view/',ViewUser.as_view(),name = "view_user"),
]