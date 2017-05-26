from django.conf.urls import url,include
from .views import (UserLoginView, UserChangeNameView,
                     UserDetailView, UserCreateView, YzmView)



urlpatterns = [
    url(r'^detail/$', UserDetailView.as_view(), name='user_detail'),
    url(r'^login/$', UserLoginView.as_view(), name='login'),
    #url(r'^logout/$', Us)
    url(r'^reg/$', UserCreateView.as_view(), name='reg'),
   # url(r'^Pro_reg/$', ProUserCreateView.as_view(), name='pro_reg'),
    url(r'^yzm/', YzmView.as_view(), name='yzm'),
    url(r'^changename/$', UserChangeNameView.as_view(), name='change_name')
    #url(r'^sign/', SignInPublishView.as_view(), name='sign'),
]
