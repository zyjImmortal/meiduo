# Create your views here.
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from users import constants
from users.models import User, Address
from users.serializers import CreateUserSerializer, UserDetailSerializer, EmailSerializer, AddressSerializer
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


class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Address模型中关联了User,通过addresses
        return self.request.user.addresses.filter(is_deleted=False)

    def list(self, request, *args, **kwargs):
        query_set = self.get_queryset()
        # 如果要被序列化的是包含多条数据的查询集QuerySet，可以通过添加many=True参数补充说明
        serializer = AddressSerializer(query_set, many=True)
        user = self.request.user
        return Response({
            'user_id': user.id,
            'limit': constants.USER_ADDRESS_COUNTS_LIMIT,
            'default_address_id': user.default_address_id,
            'addresses': serializer.data
        })

    def create(self, request, *args, **kwargs):
        """
           保存用户地址数据
        """
        # 检查用户地址数据数目不能超过上限
        count = request.user.addresses.count()
        if count >= constants.USER_ADDRESS_COUNTS_LIMIT:
            return Response({'message': '保存地址数据已达到上限'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        address = self.get_object()
        address.is_deleted = True
        address.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=True)  # detail=True表示使用通过URL获取的主键对应的数据对象
    def status(self, request, pk=None, address_id=None):
        """
        设置默认地址
        :param request:
        :param pk:
        :param address_id:
        :return:
        """
        address = self.get_object()
        request.user.default_address = address
        request.user.save()
        return Response({"message": "ok"}, status=status.HTTP_200_OK)

    @action(methods=['put'], detail=True)
    def title(self, request, pk=None, address_id=None):
        address = self.get_object()
        serializer = AddressSerializer(instance=address, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
