from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.views import View
from rest_framework.views import APIView
from users.api.serializers import RegistrationSerializers
from users.api.serializers import LoginSerializers
from users.api.serializers import UpdateSerializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import login,logout,authenticate,decorators
from users.models import User


@api_view(['POST',])
def register_api(request):
    if request.method=='POST':
        serializers = RegistrationSerializers(data=request.data)
        message ={}
        data = {}
        if serializers.is_valid():
            user = serializers.save()
            message['status'] = status.HTTP_200_OK
            message['message'] = 'OK'
            data['email'] = user.email
            data['username'] = user.username
            data['phone'] = user.phone
            data['company'] = user.company
            data['token'] = Token.objects.get(user=user).key
            message['data'] = data
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


@api_view(['POST',])
def login_api(request):
    if request.method == 'POST':
        serializers = LoginSerializers(data=request.data)
        message = {}
        try:
            serializers.is_valid(raise_exception=True)
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request,user)
                message['status'] = status.HTTP_200_OK
                message['message'] = "OK"
                message['data']= Token.objects.get(user=user).key
                return Response(message)
        except:
            message['status'] = status.HTTP_400_BAD_REQUEST
            your_error = serializers.errors
            error = your_error.values()
            for item in error:
                fail = item[0]
                break
            message['message'] = fail
            message['data'] = "null"
            return Response(message)


@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def view_api(request):
    user = request.user
    message = {}
    data = {}
    message['status'] = status.HTTP_200_OK
    message['message'] = "OK"
    data['email'] = user.email
    data['username'] = user.username
    data['phone'] = user.phone
    data['company'] = user.company
    data['sex'] = user.sex
    message['data'] = data
    return Response(message)

@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def update_user_api(request):
    message = {}
    data = {}
    try:
        user = request.user
    except user.DoesNotExist:
        message['status'] = status.HTTP_404_NOT_FOUND
        message['message'] = "user is not exist"
        message['data'] = "null"
        return Response(message)

    if request.method == "PUT":
        serializers = UpdateSerializers(user,data=request.data)
        if serializers.is_valid():
            serializers.save()
            message['status'] = status.HTTP_200_OK
            message['message'] = "oke"
            data['username'] = user.username
            data['phone'] = user.phone
            data['company'] = user.company
            data['date_of_birth'] = user.date_of_birth
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