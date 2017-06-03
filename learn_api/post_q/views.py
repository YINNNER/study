from django.shortcuts import render
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,

)
from .models import Course, Question, Post, Comment
from .serializers import (
    QuestionCreateSerializer,
    QuestionDetailSerializer,
    PostCreateSerializer,
    PostDetailSerializer,
    CourseCreateSerializer,
    CourseDetailSerializer,
    CommentCreateSerializer,
    CommentDetailSerializer,
    JoinCourseSerializer,
    FindCourseSerializer,
    GroupDetailSerializer,
    SignInSerializer,
)
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.response import Response
from .paginator import getPages
from django.contrib.auth.models import Group
from django.utils import timezone
from account.models import WHU
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
import pytz
# Create your views here.


class QuestionView(APIView):
    serializer_class = QuestionCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        serializer = QuestionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.validated_data['title']
        content = serializer.validated_data['content']
        user = request.user
        question = Question.objects.create(author=user, title=title, content=content)
        question.save()
        reply = {"msg": "Create Question Successfully"}
        response = Response(reply, HTTP_200_OK)
        return response

    def get(self, request):
        #current_page = request.GET.get("page", 1)
        queryset = Question.objects.all().order_by('-created')
        #pages, posts = getPages(request, queryset)
        serializer = QuestionDetailSerializer(queryset, data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data, HTTP_200_OK)
        return response


class QuestionDetailView(APIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication]
    content = {}

    def post(self, request, pk):
        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        content = serializer.validated_data['content']
        # question = serializer.validated_data['question']
        question = Question.objects.get(pk=pk)
        print(question.title)
        user = request.user
        comments = Comment.objects.create(author=user, content=content, question=question)
        comments.save()
        reply = {'msg': 'Create Successfully'}
        response = Response(reply, HTTP_200_OK)
        return response


    def get(self, request, pk):
        question = Question.objects.filter(pk=pk)
        if len(question) == 0:
            content = {'error': "Can't find the question"}
            response = Response(content, HTTP_404_NOT_FOUND)
            return response
        serializer = QuestionDetailSerializer(question, data=request.data, many=True)
        if serializer.is_valid(raise_exception=True):
            response = Response(serializer.data, HTTP_200_OK)
            return response
        else:
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)


class PostView(APIView):
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        user = request.user
        whu = WHU.objects.get(user=user).is_teacher
        if whu is True:
            serializer = PostCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            title = serializer.validated_data['title']
            content = serializer.validated_data['content']
            course = serializer.validated_data['course']
            files = serializer.validated_data['files']
            posts = Post.objects.create(author=user, title=title, content=content, course=course, files=files)
            posts.save()
            reply = {"msg": "Create Question Successfully"}
            response = Response(reply, HTTP_200_OK)
            return response
        else:
            reply = {'msg': "You don't own the permission"}
            response = Response(reply, HTTP_200_OK)
            return response
    def get(self, request):
        queryset = Post.objects.all().order_by('-created')
        serializer = PostDetailSerializer(queryset, data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data, HTTP_200_OK)
        return response


class PostDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    content = {}

    def get(self, request, pk):
        posts = Post.objects.filter(pk=pk)
        if len(posts) == 0:
            content = {'error': "Can't find the post"}
            response = Response(content, HTTP_404_NOT_FOUND)
            return response
        serializer = PostDetailSerializer(posts, data=request.data, many=True)
        if serializer.is_valid(raise_exception=True):
            response = Response(serializer.data, HTTP_200_OK)
            return response
        else:
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = request.user
        try:
            posts = Post.objects.get(user=user,pk=pk)
            try:
                posts.delete()
                content = {'msg': 'Delete Successfully'}
                response = Response(content, HTTP_200_OK)
                return response
            except:
                content = {'msg': 'Delete failed'}
                response = Response(content, HTTP_400_BAD_REQUEST)
                return response
        except Post.DoesNotExist:
            content = {'msg': "Can't find the post"}
            response = Response(content, HTTP_400_BAD_REQUEST)
            return response


class CourseView(APIView):
    serializer_class = CourseCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        teacher = request.user
        whu = WHU.objects.get(user=teacher).is_teacher
        if whu is True:
            serializer = CourseCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            name = serializer.validated_data['name']
            content = serializer.validated_data['content']
            course = Course.objects.create(teacher=teacher, name=name, content=content)
            course.save()
            course_group = Group.objects.create(name=name+'-'+teacher.first_name)
            teacher.groups.add(course_group)
            reply = {'msg': 'Create course successfully'}
            response = Response(reply, HTTP_200_OK)
            return response
        else:
            reply = {'msg': "You don't own the permission"}
            response = Response(reply, HTTP_200_OK)
            return response

    def get(self, request):
        queryset = Course.objects.all()
        serializer = CourseDetailSerializer(queryset, data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data, HTTP_200_OK)
        return response


class CourseDetailView(APIView):
    serializer_class = SignInSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication]
    content = {}

    def post(self, request, pk):        #签到功能
        user = request.user
        whu = WHU.objects.get(user=user)
        x = str(timezone.now().year) + '-' + str(timezone.now().month) + '-'
        y = str(timezone.now().day) + '-' + str(timezone.now().hour)
        h = x + y
        course = Course.objects.get(pk=pk)
        #如果是老师
        if whu.is_teacher is True:
            serializer = SignInSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            sign_in = serializer.validated_data['sign_in']
            if course.sign_in is False:
                try:
                    group = Group.objects.create(name=user.username + "-" + h + '时')
                    Course.objects.filter(pk=pk).update(sign_in=sign_in)
                    user.groups.add(group)
                    reply = {'msg': 'Publish Successfully'}
                except:

                    reply = {'msg': 'Today you have published it'}
            else:
                Course.objects.filter(pk=pk).update(sign_in=sign_in)
                reply = {'msg': 'Close Successfully'}
            response = Response(reply, HTTP_200_OK)
            return response
        #如果是学生
        else:
            if course.sign_in is True:
                group = Group.objects.get(name=course.teacher.username + "-" + h + '时')
                user.groups.add(group)
                reply = {'msg': 'Sign In Successfully'}
                response = Response(reply, HTTP_200_OK)
                return response
            else:
                reply = {'msg': "You can't sign in now!"}
                response = Response(reply, HTTP_200_OK)
                return response



    def get(self, request, pk):
        course = Course.objects.filter(pk=pk)
        if len(course) == 0:
            content = {'error': "Can't find the course"}
            response = Response(content, HTTP_404_NOT_FOUND)
            return response
        serializer = CourseDetailSerializer(course, data=request.data, many=True)
        if serializer.is_valid(raise_exception=True):
            response = Response(serializer.data, HTTP_200_OK)
            return response
        else:
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)


class CommentView(APIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication]


    def get(self, request, pk):
        queryset = Comment.objects.fitler(pk=pk)
        serializer = CommentDetailSerializer(queryset, data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data, HTTP_200_OK)
        return response


# class CommentDetailView(APIView):
#
#     permission_classes = [IsAuthenticated]
#     content = {}
#
#     def get(self, request, pk):
#         course = Comment.objects.filter(pk=pk)
#         if len(course) == 0:
#             content = {'error': "Can't find the course"}
#             response = Response(content, HTTP_404_NOT_FOUND)
#             return response
#         serializer = CommentDetailSerializer(course, data=request.data, many=True)
#         if serializer.is_valid(raise_exception=True):
#             response = Response(serializer.data, HTTP_200_OK)
#             return response
#         else:
#             return Response(serializer.errors, HTTP_400_BAD_REQUEST)


class FindCourseView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = FindCourseSerializer
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        serializer = FindCourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data['name']
        queryset = Course.objects.filter(Q(name__icontains=name) | Q(content__icontains=name))
        serializer = CourseDetailSerializer(queryset, data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data, HTTP_200_OK)
        return response

    def get(self, request):
        queryset = Course.objects.all()
        serializer = CourseDetailSerializer(queryset, data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data, HTTP_200_OK)
        return response


class AddCourseView(APIView):
    serializer_class = JoinCourseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        user = request.user
        whu = WHU.objects.get(user=user).is_teacher
        if whu is False:
            serializer = JoinCourseSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            name = serializer.validated_data['name']
            teacher = serializer.validated_data['teacher']
            cs = Group.objects.get(name=name+'-'+teacher.first_name)
            user.groups.add(cs)
            reply = {'msg': 'Join successfully'}
            response = Response(reply, HTTP_200_OK)
            return response
        else:
            reply = {'msg': "You are a teacher, so you needn't join it"}
            response = Response(reply, HTTP_200_OK)
            return response

    def get(self, request):
        queryset = Course.objects.all()
        serializer = CourseDetailSerializer(queryset, data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data, HTTP_200_OK)
        return response


# class SignInPublishView(APIView):
#     serializer_class = SignInSerializer
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [SessionAuthentication]
#
#     def post(self, request, pk):
#         serializer = SignInSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         sign_in = serializer.validated_data['sign_in']
#         user = request.user
#         x = str(timezone.now().year)+'-'+str(timezone.now().month)+'-'
#         y = str(timezone.now().day)+'  '+str(timezone.now().hour)
#         h = x+y
#         Course.objects.filter(pk=pk).update(sign_in=sign_in)
#         group = Group.objects.create(name=user.username+"-"+h+'时')
#         user.groups.add(group)
#         reply = {'msg': 'Publish Successfully'}
#         response = Response(reply, HTTP_200_OK)
#         return response
