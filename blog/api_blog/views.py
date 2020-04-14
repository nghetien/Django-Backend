from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from blog.api_blog.serializers import BlogPostSerializers
from django.utils.text import slugify
from blog.api_blog.serializers import CommentBlogSerializers
from blog.models import Blog,CommentBlog
from django.shortcuts import get_object_or_404

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
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
@permission_classes((IsAuthenticated,))
def update_blog_api(request,slug):
    message = {}
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        message['status'] = status.HTTP_404_NOT_FOUND
        message['message'] = "Blog is not exist"
        message['data'] = "null"
        return Response(message)

    user = request.user
    if not user.is_superuser:
        message['status'] = status.HTTP_400_BAD_REQUEST
        message['message'] = "You dont have permission"
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
@permission_classes((IsAuthenticated,))
def delete_blog_api(request,slug):
    message = {}
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        message['status'] = status.HTTP_404_NOT_FOUND
        message['message'] = "Blog is not exist"
        message['data'] = "null"
        return Response(message)

    user = request.user
    if not user.is_superuser:
        message['status'] = status.HTTP_400_BAD_REQUEST
        message['message'] = "You dont have permission"
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
@permission_classes((IsAuthenticated,))
def post_blog_api(request):
    message = {}
    user = request.user
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




@api_view(['GET',])
def detail_comment_blog_api(request,slug):
    message = {}
    data = {}
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        message['status'] = status.HTTP_404_NOT_FOUND
        message['message'] = "Blog is not exist"
        message['data'] = "null"
        return Response(message)
    all_comment = CommentBlog.objects.filter(name_blog=blog)
    if request.method == "GET":
        serializer = CommentBlogSerializers(all_comment,many=True)
        my_data = serializer.data
        cmt = "commnet"
        run = 1
        temp = cmt+str(run)
        for item in my_data:
            data[temp] = item
            run = run+1
            temp = cmt + str(run)
        message['status'] = status.HTTP_200_OK
        message['message'] = "OK"
        message['data'] = data
        return Response(message)

@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def update_commnet_blog_api(request,slug,id):
    message = {}
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        message['status'] = status.HTTP_404_NOT_FOUND
        message['message'] = "Blog is not exist"
        message['data'] = "null"
        return Response(message)

    try:
        my_comment = get_object_or_404(CommentBlog, id=id)
    except:
        message['status'] = status.HTTP_404_NOT_FOUND
        message['message'] = "Commnet is not exist"
        message['data'] = "null"
        return Response(message)
    user = request.user
    if (my_comment.author != user and user.is_superuser==False):
        message['status'] = status.HTTP_404_NOT_FOUND
        message['message'] = "You dont have permission"
        message['data'] = "null"
        return Response(message)

    if request.method == "PUT":
        serializers = CommentBlogSerializers(my_comment,data = request.data)
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
@permission_classes((IsAuthenticated,))
def delete_comment_blog_api(request,slug,id):
    message = {}
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        message['status'] = status.HTTP_404_NOT_FOUND
        message['message'] = "Blog is not exist"
        message['data'] = "null"
        return Response(message)

    try:
        my_comment = get_object_or_404(CommentBlog,id=id)
    except:
        message['status'] = status.HTTP_404_NOT_FOUND
        message['message'] = "Commnet is not exist"
        message['data'] = "null"
        return Response(message)
    user = request.user
    if (my_comment.author != user and user.is_superuser==False):
        message['status'] = status.HTTP_404_NOT_FOUND
        message['message'] = "You dont have permission"
        message['data'] = "null"
        return Response(message)
    if request.method == "DELETE":
        operation = my_comment.delete()
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
@permission_classes((IsAuthenticated,))
def post_comment_blog_api(request,slug):
    message = {}
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        message['status'] = status.HTTP_404_NOT_FOUND
        message['message'] = "Blog is not exist"
        message['data'] = "null"
        return Response(message)
    user =request.user
    my_comment = CommentBlog(author=user,name_blog=blog)
    if request.method =="POST":
        serializers = CommentBlogSerializers(my_comment,data=request.data)
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