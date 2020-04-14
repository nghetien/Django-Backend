from django.urls import path
from blog.api_blog.views import detail_blog_api,post_blog_api,update_blog_api,delete_blog_api
from blog.api_blog.views import detail_comment_blog_api,delete_comment_blog_api,update_commnet_blog_api,post_comment_blog_api
app_name = 'blog_api'

urlpatterns =[
    path('<slug>/',detail_blog_api,name="detail-blog"),
    path('<slug>/update',update_blog_api,name="update-blog"),
    path('<slug>/delete',delete_blog_api,name="delete-blog"),
    path('post-blog',post_blog_api,name="post-blog"),
    path('<slug>/detail-comment',detail_comment_blog_api,name="detail_comment_blog_api"),
    path('<slug>/comment/<id>/update',update_commnet_blog_api,name="update_commnet_blog_api"),
    path('<slug>/comment/<id>/delete',delete_comment_blog_api,name="delete_commnet_blog_api"),
    path('<slug>/comment',post_comment_blog_api,name="post_commnet_blog_api"),
]