from django.conf.urls import url,include
from .views import (QuestionView,
                    QuestionDetailView,
                    PostDetailView,
                    PostView,
                    CourseView,
                    CourseDetailView,
                    CommentView,
                   # CommentDetailView,
                    AddCourseView,
                    FindCourseView,
                    #SignInPublishView,
                    )
urlpatterns = [
    url(r'^post/$', PostView.as_view(), name='post'),
    url(r'^post/(?P<pk>\d+)', PostDetailView.as_view(), name='post_detail'),
    url(r'^question/$', QuestionView.as_view(), name='question'),
    url(r'^question/(?P<pk>\d+)', QuestionDetailView.as_view(), name='Q_detail'),
    url(r'^course/$', CourseView.as_view(), name='course'),
    url(r'^course/(?P<pk>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
   # url(r'^question/(?P<pk>\d+)/comment/', CommentCreateView.as_view(), name='comment'),
    url(r'^question/(\d+)/comment/', CommentView.as_view(), name='comment'),
    url(r'^add_course/', AddCourseView.as_view(), name='add_course'),
    url(r'^f_course/', FindCourseView.as_view(), name='f_course'),
    url(r'^search/', include('haystack.urls')),
    #   url(r'^course/(<?P<pk>\d+)/sign_in/', SignInPublishView.as_view(), name='sign'),

]
