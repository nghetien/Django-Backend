from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import login,logout,authenticate,decorators
from django.contrib.auth.hashers import make_password
from users.forms import RegisterForm,UserAuthenticateForm,UserUpdatingForm
from users.models import User
# from accesstoken.models import AccessToken
import hashlib
from datetime import datetime


# Create your views here.


def home(request):
    return render(request,"WebLab_ver4/index.html")

class Login(View):
    def get(self,request):
        context = {}
        form = UserAuthenticateForm()
        context['form'] = form
        return render(request,'WebLab_ver4/login.html',context)
    def post(self,request):
        context = {}
        form = UserAuthenticateForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email,password=password)
            if user:
                login(request,user)
                # now = datetime.now()
                # timestamp = datetime.timestamp(now)
                # string = email + '-' + str(timestamp)
                # ac_tk = AccessToken(access_token=string).save()
                # ac_tk.email_user = request.user.email
                # ac_tk.save()
                return redirect("home")
        else: # return lại lỗi tự form
            context['form'] = form
            return render(request, "WebLab_ver4/login.html", context)

class Logout(View):
    def get(self,request):
        logout(request)
        return redirect("home")

class Register(View):
    def get(self,request):
        context = {}
        form = RegisterForm()
        context['form'] = form
        return render(request,"WebLab_ver4/register.html",context)
    def post(self,request):
        context = {}
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email,password=raw_password)
            login(request,account)
            return redirect("home")
        else:
            context['form'] = form
            return render(request,"WebLab_ver4/register.html",context)


class Updating(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect("login")
        else:
            context = {}
            form = UserUpdatingForm( # giá trị mặc định khi bắt đầu vào update
                initial={
                    "username": request.user.username,
                    "date_of_birth" :request.user.date_of_birth,
                    "phone":request.user.phone,
                    "company":request.user.company,
                    "address":request.user.address,
                }
            )
            context['form'] = form
            return render(request, "WebLab_ver4/updating.html", context)
    def post(self,request):
        form = UserUpdatingForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("home")
class ViewUser(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect("login")
        else:
            context = {}
            my_user =  User.objects.all()
            context['my_user']= my_user
            return render(request,"WebLab_ver4/view_user.html",context)