from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly
)
from .models import WHU, SignIn
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.models import User, Permission, Group
# Create your views here.
from .serializers import (
    UserCreateSerializer,
    WHUCreateSerializer,
    WhuDetailSerializer,
    UserLoginSerializer,
    UserChangeNameSerializer,
    )
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND, )
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from .spider import spider, save_img
from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType
import requests
from django.contrib.auth.decorators import login_required
from django.utils import timezone

class UserCreateView(APIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        yzm_text = serializer.validated_data['yzm_text']
        yzm_cookie = serializer.validated_data['yzm_cookie']

        try:
            spider(username, password, yzm_text, yzm_cookie)
            user_obj = User(username=username)
            user_obj.set_password(password)
            user_obj.save()
            if len(username) == 13:
                stu_group = Group.objects.get(name="student")
                user_obj.groups.add(stu_group)
            else:
                pro_group = Group.objects.get(name='teacher')
                user_obj.groups.add(pro_group)
            # content_type = ContentType.objects.get(model='WHU')
            # pro_permission = Permission.objects.create(codename='has_publish_signin',
            #                                            name='Can publish',
            #                                            content_type=content_type)
            # user_obj.user_permissions.add(pro_permission)
            try:
                if len(username) == 13:
                    student = WHU.objects.create(user=user_obj, is_teacher=False)
                    student.save()
                else:
                    teacher = WHU.objects.create(user=user_obj, is_teacher=True)
                    teacher.save()
                content = {'msg': 'Create user successful'}
                return Response(content, HTTP_200_OK)
            except Exception as e:
                # print e.message
                reply = {'error': 'Create user_student failed'}
                return Response(reply, HTTP_400_BAD_REQUEST)
        except:
            reply = {'error': 'Create user failed'}
            return Response(reply, HTTP_400_BAD_REQUEST)

    def get(self, request):
        queryset = WHU.objects.all()
        serializer = WhuDetailSerializer(queryset, data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data, HTTP_200_OK)
        return response



class UserLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data['username']
            password = serializer.data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                # print "user is not none"
                if user.is_active:
                    login(request, user)
                    content = {'msg': 'Login successful'}
                    return Response(content, HTTP_200_OK)
            else:
                reply = {'error': 'Login failed'}
                return Response(reply, HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# class ProUserCreateView(APIView):
#     serializer_class = UserCreateSerializer
#     permission_classes = [AllowAny]
#     authentication_classes = [SessionAuthentication]

#     def post(self, request):
#         serializer = UserCreateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         username = serializer.validated_data['username']
#         password = serializer.validated_data['password']
#         yzm_text = serializer.validated_data['yzm_text']
#         yzm_cookie = serializer.validated_data['yzm_cookie']
#         reply = {}
#         if spider(username, password, yzm_text, yzm_cookie) is True:
#             user_obj = User(username=username)
#             user_obj.set_password(password)
#             user_obj.save()
#             pro_group = Group.objects.get(name='teacher')
#             user_obj.groups.add(pro_group)
#             # content_type = ContentType.objects.get(model='WHU')
#             # pro_permission = Permission.objects.create(codename='has_publish_signin',
#             #                                            name='Can publish signin',
#             #                                            content_type=content_type)
#             # user_obj.user_permissions.add(pro_permission)
#             try:
#                 pro = WHU.objects.create(user=user_obj, is_teacher=True)
#                 pro.save()
#                 content = {'msg': 'Create user successful'}
#                 return Response(content, HTTP_200_OK)
#             except Exception as e:
#                 # print e.message
#                 reply = {'error': 'Create user_student failed'}
#                 return Response(reply, HTTP_400_BAD_REQUEST)
#         else:
#             reply = {'error': 'Create user failed'}
#             return Response(reply, HTTP_400_BAD_REQUEST)



class UserDetailView(APIView):
    serializer_class = WhuDetailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        queryset =WHU.objects.all()
        serializer = WhuDetailSerializer(queryset, data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data, HTTP_200_OK)
        return response


class YzmView(APIView):
    def get(self, request):
        username = request.user.username
        image_url = 'http://210.42.121.241/servlet/GenImg'
        yzm = requests.get(image_url)
        yzm_image = yzm.content
        save_img(username, yzm_image)
        yzm_url = "/media/yzm/" + str(username) + ".jpg"
        yzm_cookie = yzm.headers['Set-Cookie']
        content = {}
        content['yzm_url'] = yzm_url
        content['yzm_cookie'] = yzm_cookie
        response = Response(content, HTTP_200_OK)
        return response


class UserChangeNameView(APIView):
    serializer_class = UserChangeNameSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        serializer = UserChangeNameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        nickname = serializer.validated_data['first_name']
        user = request.user
        User.objects.filter(username=user.username).update(first_name=nickname)
        reply = {'msg': 'Change Successfully'}
        response = Response(reply, HTTP_200_OK)
        return response


    def get(self, request):
        user = request.user
        queryset = User.objects.filter(username=user.username)
        serializer = WhuDetailSerializer(queryset, data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data, HTTP_200_OK)
        return response




















