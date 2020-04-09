from django.urls import path
from users.api.views import register_api,login_api,view_api



urlpatterns =[
    path('register/',register_api,name="register"),
    path('login/',login_api,name="login"),
    path('view-user/',view_api,name="view-user"),
]