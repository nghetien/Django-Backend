from django.urls import path
from blog.api_blog.views import detail_blog_api,post_blog_api,update_blog_api,delete_blog_api
app_name = 'blog_api'

urlpatterns =[
    path('<slug>/',detail_blog_api,name="detail-blog"),
    path('<slug>/update',update_blog_api,name="update-blog"),
    path('<slug>/delete',delete_blog_api,name="delete-blog"),
    path('post-blog',post_blog_api,name="post-blog"),
]