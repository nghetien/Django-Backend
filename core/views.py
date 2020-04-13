from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
#---------------------------------------------------------------------
from django.contrib.auth import login,logout,authenticate,decorators
from django.contrib.auth.hashers import make_password
#---------------------------------------------------------------------
from users.forms import RegisterForm,UserAuthenticateForm,UserUpdatingForm
from users.models import User
#---------------------------------------------------------------------
import hashlib
from datetime import datetime
#---------------------------------------------------------------------
from blog.models import Blog,ImageBlog
from blog.forms import CreateBlogForm
#---------------------------------------------------------------------
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

class PostBlog(View):
    def get(self,request):
        context = {}
        user = request.user
        if not user.is_authenticated:
            return redirect("home")
        else:
            form = CreateBlogForm()
            context['form'] = form
            return render(request,"WebLab_ver4/new_post.html",context)
    def post(self,request):
        context = {}
        user = request.user
        if not user.is_authenticated:
            return redirect("home")
        else:
            form = CreateBlogForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                obj = form.save(commit=False)
                author = User.objects.filter(email=user.email).first()
                obj.author = author
                obj.save()
                return redirect("home")
            else:
                return HttpResponse("that bai")

class ViewBlog(View):
    def get(self,request):
        context = {}
        form = Blog.objects.all()
        context['form'] = form
        return render(request,"WebLab_ver4/view_blog.html",context)

