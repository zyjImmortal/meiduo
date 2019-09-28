# Create your views here.
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework import status

from users.models import User
from users.serializers import CreateUserSerializer, UserDetailSerializer, EmailSerializer
from users.utils import get_user_by_account
from verifications.serializers import CheckImageCodeSerializer
import re


class UserView(CreateAPIView):
    serializer_class = CreateUserSerializer


class UsernameCountView(APIView):

    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        data = {
            "username": username,
            "count": count
        }
        return Response(data)


class MobileCountView(APIView):
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        data = {
            "mobile": mobile,
            "count": count
        }
        return Response(data)


class SmsCodeTokenView(GenericAPIView):
    """获取发送短信验证码的t凭据"""
    serializer_class = CheckImageCodeSerializer

    def get(self, request, account):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        user = get_user_by_account(account)
        if user is not None:
            return Response({'message': "用户不存在"}, status=status.HTTP_404_NOT_FOUND)
        token = user.generate_sms_access_token()
        # 将手机号中间4位替换掉
        mobile = re.sub(r'(\d{3})\d{4}(\d{4})', r'\1****\2', user.mobile)
        data = {
            'mobile': mobile,
            'access_token': token
        }
        return Response(data)


class UserDetailView(RetrieveAPIView):
    """
    RetrieveModelMixin扩展类,提供一个模型对象的基本信息

    为什么重写get_object()方法，这个方法从查询集中通过路径传过来的ID获取某个对象
        但是，现在路径中没有参数，是通过请求的token中获取

    如何获取用户对象： 在请求进入drf后，会根据header的token去获取用户信息，并存在到request对象的user属性中

    类视图属性
        request ，请求上下文对象
        kwargs 传给视图的参数
    """

    # query_set = User.objects.all()  # 为GenericAPIView提供一个查询集,供self.get_object()方法使用
    serializer_class = UserDetailSerializer

    # 配置权限,通过认证才能访问
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """

        :return User 返回请求的用户对象
        """
        return self.request.user


class EmailView(UpdateAPIView):

    def get_object(self):
        return self.request.user

    def get_serializer(self, *args, **kwargs):
        return EmailSerializer(self.request.user, data=self.request.data)


class EmailVerifyView(APIView):
    """邮箱验证"""

    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({"缺少token"}, status=status.HTTP_400_BAD_REQUEST)
        result = User.check_email_verify_token(token)
        if result:
            return Response({"message": "ok"})
        else:
            return Response({"message": "非法的token"}, status=status.HTTP_400_BAD_REQUEST)
