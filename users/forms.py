from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text="Requied. Add a valid email address")

    class Meta:
        model = User
        fields = ('email','username','phone','company','password1','password2')


class UserAuthenticateForm(forms.ModelForm):
    password = forms.CharField(label="Password",widget=forms.PasswordInput)

    class Meta:
        model= User
        fields = ('email','password')

    def clean(self): # hàm kiểm tra
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email,password=password):
                raise forms.ValidationError("Invalid login")

class UserUpdatingForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username','date_of_birth','phone','company','address')

    def clean_username(self): # kiểm tra
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                user = User.objects.exclude(pk=self.instance.pk).get(username=username)
            except User.DoesNotExist: # nếu không tồn tại thì return lại username
                return username
            raise forms.ValidationError('User "%s" is already in use' % user.username)
            # nếu tồn tại ruturn lại lỗi


