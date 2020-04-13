from django.urls import path
from users.api_user.views import register_api,login_api,view_api,update_user_api
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'user_api'

urlpatterns =[
    path('register/',register_api,name="register"),
    path('login/',login_api,name="login"),
    path('view-user/',view_api,name="view-user"),
    path('update-user/',update_user_api,name="update-user"),
]