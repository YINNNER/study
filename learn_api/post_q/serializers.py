from rest_framework.serializers import (
    CharField,
    EmailField,
    ImageField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
)

from .models import Question, Post, Course, Comment
from django.contrib.auth.models import Group


class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'course',
            'files',
        ]

    def validata(self, data):
        title = data.get('title')
        content = data.get('content')
        if not title:
            raise ValidationError('No Title')
        if not content:
            raise ValidationError("No Content")
        return data


class PostDetailSerializer(ModelSerializer):
    author = SerializerMethodField()
    pk = SerializerMethodField()
    course = SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'author',
            'pk',
            'created',
            'course',
            'files',
        ]

    def get_author(self, obj):
        return obj.author.username

    def get_pk(self, obj):
        return obj.pk

    def get_course(self, obj):
        return obj.course.name

class QuestionCreateSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'title',
            'content',
        ]

    def validata(self, data):
        title = data.get('title')
        content = data.get('content')
        if not title:
            raise ValidationError('No Title')
        if not content:
            raise ValidationError("No Content")
        return data


class QuestionDetailSerializer(ModelSerializer):
    author = SerializerMethodField()
    pk = SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            'title',
            'content',
            'author',
            'pk',
            'created',
        ]

    def get_author(self, obj):
        return obj.author.username

    def get_pk(self, obj):
        return obj.pk


class CourseCreateSerializer(ModelSerializer):
    class Meta:

        model = Course
        fields = [
            'name',
            'content',
        ]

    def validata(self, data):
        name = data.get('name')
        content = data.get('content')
        if not name:
            raise ValidationError('No name')
        if not content:
            raise ValidationError('No content')


class CourseDetailSerializer(ModelSerializer):

    teacher = SerializerMethodField()
    pk = SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'teacher',
            'name',
            'pk',
            'content',
            'sign_in',
            'student_num',
        ]

    def get_teacher(self, obj):
        return obj.teacher.username

    def get_pk(self, obj):
        return obj.pk


class FindCourseSerializer(ModelSerializer):

    class Meta:
        model = Course
        fields = [
            'name',
        ]

    def validata(self, data):
        name = data.get('name')
        if not name:
            raise ValidationError('No name')


class JoinCourseSerializer(ModelSerializer):

    class Meta:
        model = Course
        fields = [
            'name',
            'teacher',
       ]

class CommentCreateSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            'content',
            #'question',
        ]

    def validata(self, data):
        content = data.get('content')
        if not content:
            raise ValidationError('No content')


class CommentDetailSerializer(ModelSerializer):
    author = SerializerMethodField()
    question = SerializerMethodField()
    pk = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'content',
            'question',
            'pk',
            'author',
            'created',
        ]

    def get_pk(self, obj):
        return obj.pk

    def get_question(self, obj):
        return obj.question.title

    def get_author(self, obj):
        return obj.author.username


class GroupDetailSerializer(ModelSerializer):

    class Meta:
        model = Group
        fields = [
            'name',
       ]


class SignInSerializer(ModelSerializer):

    class Meta:
        model = Course
        fields = [
            'sign_in',
           # 'del_sign_in',
        ]


