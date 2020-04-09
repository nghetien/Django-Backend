from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class UserManager(BaseUserManager):
    def create_user(self,email,username,phone,password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an email username")
        if not phone:
            raise ValueError("Users must have an email numberphone")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone=phone,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_staffuser(self,email,username,phone,password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            phone=phone,
        )

        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,phone,password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            phone=phone,
        )

        user.is_admin=True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True)
    username = models.CharField(max_length=30,unique=True,)
    date_joined = models.DateTimeField(verbose_name='date joined',auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='late login',auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_of_birth = models.DateTimeField(verbose_name='date of birth',null=True)
    phone = models.CharField(verbose_name='phone',max_length=15)
    company = models.CharField(verbose_name='company',max_length=20)
    address = models.CharField(verbose_name='address', max_length=20)

    USERNAME_FIELD = 'email'  # user chính dùng là email
    REQUIRED_FIELDS = ['username','phone'] # bắt buộc phải có

    objects = UserManager()

    def __str__(self): #hiện email trong thanh tìm kiếm
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


@receiver(post_save,sender = settings.AUTH_USER_MODEL)
def CreateAuthToken(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)