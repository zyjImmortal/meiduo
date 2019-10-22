from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from . import views

router = DefaultRouter()
router.register('addresses', views.AddressViewSet, base_name='address')

urlpatterns = [
    url(r'^register', views.UserView.as_view()),
    url(r'^usernames/(?P<username>\w{5,20})', views.UsernameCountView.as_view()),
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})', views.MobileCountView.as_view()),
    url(r'^authorizations/$', obtain_jwt_token),  # 登陆获取token
    url(r'user', views.UserDetailView.as_view()),  # 用户个人详情
    url(r'emails/$', views.EmailView.as_view()),
    url(r'emails/verification/$', views.EmailVerifyView.as_view()),
    # url(r'addresses', views.AddressViewSet.as_view({'get': 'list'}))
]

urlpatterns += router.urls
