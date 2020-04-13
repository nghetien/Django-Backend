from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from rest_framework import status
from blog.models import Blog

class BlogPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title','body','image_cover','date_update',]