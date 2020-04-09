from rest_framework import serializers
from users.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from rest_framework import status

class RegistrationSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model = User
        fields = ['email','username','phone','company','password','password2']
        extra_kwargs = {
                'password': {'write_only': True}
        }


    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password!=password2:
            message = {}
            message['status'] = status.HTTP_400_BAD_REQUEST
            message['message'] = "Password2 and Password are different "
            message['data'] = "null"
            raise serializers.ValidationError(message)

        user = User(
            email=self.validated_data['email'],
            username = self.validated_data['username'],
            phone= self.validated_data['phone'],
            company=self.validated_data['company'],
        )

        user.set_password(password)
        user.save()
        return user

class LoginSerializers(serializers.ModelSerializer):

    email = serializers.EmailField(label="Email Address")
    class Meta:
        model= User
        fields = ['email','password',]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)
            if not user:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError('Must include "username" and "password".')

        data['user'] = user
        return data

# class UpdateSerializers(serializers.ModelSerializer):
#
#     class Meta:
#         model = User
#         fields = ['username','phone','company','date_of_birth',]
#         extra_kwargs = {
#                 'password': {'write_only': True}
#         }
#
#     def save(self):
#         if self.is_valid():
#             username = self.cleaned_data['username']
#             try:
#                 user = User.objects.exclude(pk=self.instance.pk).get(username=username)
#             except User.DoesNotExist: # nếu không tồn tại thì return lại username
#                 return username
#             raise forms.ValidationError('User "%s" is already in use' % user.username)
