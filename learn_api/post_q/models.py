from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Question(models.Model):
    #author = models.ForeignKey(student)
    author = models.ForeignKey(User)
    title = models.CharField(max_length=16)
    created = models.DateField(auto_now_add=True)
    content = models.TextField(max_length=140)
    # 回复问题

    def __str__(self):
        return self.title


#公告


class Post(models.Model):
    title = models.CharField(max_length=16)
#   author = models.ForeignKey(teacher)
    author = models.ForeignKey(User)
    content = models.CharField(max_length=140)
    created = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey('Course', default=False)
    files = models.FileField(upload_to='./file/files', null=True, blank=True)

    def __str__(self):
        return self.title

#课程
class Course(models.Model):
    name = models.CharField(max_length=24)
    content = models.TextField(max_length=2048)
    teacher = models.ForeignKey(User)
    #student = models.ForeignKey()
    sign_in = models.BooleanField(default=False)
   # del_sign_in = models.NBooleanField(null=True, default=True)
    student_num = models.CharField(max_length=500,null=True)
    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey(User)
    content = models.CharField(max_length=140)
    created = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question)

    def __str__(self):
        return self.question.title
