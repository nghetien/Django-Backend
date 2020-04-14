from django.contrib import admin
from django.urls import path
from . import views
from .views import Register,Logout,Login,Updating,ViewUser,PostBlog,ViewBlog,CommentBlogView
urlpatterns = [
    path('',views.home,name="home"),
    path('register/',Register.as_view(),name="register"),
    path('logout/',Logout.as_view(),name="logout"),
    path('login/',Login.as_view(),name="login"),
    path('updating/',Updating.as_view(),name = "update"),
    path('view/',ViewUser.as_view(),name = "view_user"),
    path('postblog',PostBlog.as_view(),name= "post_blog"),
    path('viewblog',ViewBlog.as_view(),name= "view_blog"),
    path('<slug>/',CommentBlogView.as_view(),name="coment_blog_view"),
]