from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.views import View
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import login,logout,authenticate,decorators
from blog.models import Blog
from blog.api_blog.serializers import BlogPostSerializers
from users.models import User
from django.utils.text import slugify
import string

@api_view(['GET',])
def detail_blog_api(request,slug):
    message = {}
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        message['status'] = status.HTTP_404_NOT_FOUND
        message['message'] = "Blog is not exist"
        message['data'] = "null"
        return Response(message)

    if request.method == "GET":
        serializers = BlogPostSerializers(blog)
        message['status'] = status.HTTP_200_OK
        message['message'] = "OK"
        data = serializers.data
        message['data'] = data
        return Response(message)

@api_view(['PUT',])
def update_blog_api(request,slug):
    message = {}
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        message['status'] = status.HTTP_404_NOT_FOUND
        message['message'] = "Blog is not exist"
        message['data'] = "null"
        return Response(message)

    if request.method == "PUT":
        serializers = BlogPostSerializers(blog,data = request.data)
        if serializers.is_valid():
            serializers.save()
            message['status'] = status.HTTP_200_OK
            message['message'] = "OK"
            data = serializers.data
            message['data']= data
            return Response(message)
        else:
            message['status'] = status.HTTP_400_BAD_REQUEST
            your_error = serializers.errors
            error = your_error.values()
            for item in error:
                fail = item[0]
                break
            message['message'] = fail
            message['data'] = "null"
            return Response(message)

@api_view(['DELETE',])
def delete_blog_api(request,slug):
    message = {}
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        message['status'] = status.HTTP_404_NOT_FOUND
        message['message'] = "Blog is not exist"
        message['data'] = "null"
        return Response(message)

    if request.method == "DELETE":
        operation = blog.delete()
        if operation:
            message['status'] = status.HTTP_200_OK
            message['message'] = "OK"
            message['data']= "null"
            return Response(message)
        else:
            message['status'] = status.HTTP_400_BAD_REQUEST
            message['message'] = "delete failed"
            message['data'] = "null"
            return Response(message)

@api_view(['POST',])
def post_blog_api(request):
    message = {}
    user = User.objects.get(pk=1)
    username = user.username
    blog = Blog(author=user)
    if request.method =="POST":
        serializers = BlogPostSerializers(blog,data=request.data)
        title = serializers.initial_data['title']
        title = title.lower()
        title = slugify(title)
        title = '-'+title
        slug = user.username+title
        try:
            Blog.objects.get(slug=slug)
        except Blog.DoesNotExist:
            if serializers.is_valid():
                serializers.save()
                message['status'] = status.HTTP_201_CREATED
                message['message'] = "OK"
                data = serializers.data
                message['data'] = data
                return Response(message)
            else:
                message['status'] = status.HTTP_400_BAD_REQUEST
                your_error = serializers.errors
                error = your_error.values()
                for item in error:
                    fail = item[0]
                    break
                message['message'] = fail
                message['data'] = "null"
                return Response(message)
        message['status'] = status.HTTP_400_BAD_REQUEST
        message['message'] = "title is exist"
        message['data'] = "null"
        return Response(message)