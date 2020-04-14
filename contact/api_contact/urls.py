from django.urls import path
app_name = 'contact_api'
from contact.api_contact.views import contact_api

urlpatterns =[
    path('',contact_api,name="contact"),
]