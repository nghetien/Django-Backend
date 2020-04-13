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
            # lỗi không ở dạng key :[] vì đây k phải hàm if is_valid()
            # blank trong register và login(không cần seria.error vẫn tự ra lỗi)
            # register: lỗi validated_data không đọc được giá trị nhưng vẫn chạy tiếp chương trình
            # login : data.get không đọc được giá trị thì chương trình bị dừng luôn

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

    def validate(self, data): # hàm is_valid

        email = data.get('email') # nếu không nhập vào thì lỗi sẽ xuất hiện tại đây
        password = data.get('password') # nếu không nhập vào thì lỗi sẽ xuất hiện tại đây
        #lỗi sẽ in ra ở dạng key : []

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)
            if not user: # lỗi dưới dạng key:[] vì hàm if se.is_valid() lỗi
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError('Must include "username" and "password".')

        data['user'] = user
        return data

class UpdateSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username','phone','company','date_of_birth','sex',]
        extra_kwargs = {
                'password': {'write_only': True}
        }


    def create(self, slug):
        return User.objects.create_user(slug=slug)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.company = validated_data.get('company', instance.company)
        instance.sex = validated_data.get('sex', instance.sex)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance = super().update(instance, validated_data)
        return instance
class ViewSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','username','date_joined','last_login','date_of_birth',
                  'phone','company','address','sex',]