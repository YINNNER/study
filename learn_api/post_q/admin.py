from django.contrib import admin
from .models import Comment, Question, Course, Post
# Register your models here.

admin.site.register(Post)
admin.site.register(Course)
admin.site.register(Comment)
admin.site.register(Question)
