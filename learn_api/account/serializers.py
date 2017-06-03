from rest_framework.serializers import (
    CharField,
    EmailField,
    ImageField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
)
from .models import WHU, SignIn
from django.contrib.auth.models import User


class WHUCreateSerializer(ModelSerializer):
    class Meta:
        model = WHU
        fields=[
            'is_teacher',
        ]

class UserCreateSerializer(ModelSerializer):
    yzm_text = CharField()
    yzm_cookie = CharField()
    password = CharField(label='Password',
                         write_only=True,
                         style={'input_type': 'password'})
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'yzm_text',
            'yzm_cookie',
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if not username:
            raise ValidationError('lack username')
        if not password:
            raise ValidationError('lack password')
        return data

    def validate_username(self,value):
        data = self.get_initial()
        username = data.get('username')
        user_qs = User.objects.filter(username=username)
        if user_qs.exists():
            raise ValidationError("The username has been registered.")
        return value

class UserLoginSerializer(ModelSerializer):
    username = CharField()
    password = CharField(style={'input_type': 'password'})
    # password = PasswordField()
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }

class WhuDetailSerializer(ModelSerializer):
    user = SerializerMethodField()
    id = CharField()
    class Meta:
        model = WHU
        fields =[
            'user',
            'id',
            'is_teacher',
        ]

    def get_user(self, obj):
        return obj.user.username
    def get_id(self,obj):
        return obj.pk


class UserChangeNameSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            'first_name',
        ]


class UserLogoutSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
        ]


