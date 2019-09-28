from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from . import views

urlpatterns = [
    url(r'^register', views.UserView.as_view()),
    url(r'^usernames/(?P<username>\w{5,20})', views.UsernameCountView.as_view()),
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})', views.MobileCountView.as_view()),
    url(r'^authorizations/$', obtain_jwt_token),  # 登陆获取token
    url(r'user', views.UserDetailView.as_view())  # 用户个人详情
]
