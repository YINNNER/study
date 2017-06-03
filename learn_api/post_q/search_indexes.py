# -*- coding:utf-8 -*-

from .models import Course, Question, Post
from haystack import indexes
#公告搜索
class PostIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    created = indexes.DateTimeField(model_attr='created')
    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

#问题搜索
class QuestionIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    created = indexes.DateTimeField(model_attr='created')
    def get_model(self):
        return Question

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
#课程搜索
class CourseIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Course

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
