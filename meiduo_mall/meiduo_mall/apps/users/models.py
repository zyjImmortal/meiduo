from django.contrib.auth.models import AbstractUser
from django.db import models
from itsdangerous import TimedJSONWebSignatureSerializer as TJSerializer, BadData
from django.conf import settings

from . import constants


# Create your models here.


class User(AbstractUser):
    """
    扩展django自带的用户模型，增加phone字段,使用Django提供的认证系统
    """
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号")
    email_active = models.BooleanField(default=False, verbose_name="邮箱验证状态")

    class Meta:
        db_table = 'tb_users'
        verbose_name = "用户"  # 指明一个易于理解和表述的对象名称，单数形式
        verbose_name_plural = verbose_name  # 复数形式

    def generate_sms_access_token(self):
        serializer = TJSerializer(secret_key=settings.SECRET_KEY, expires_in=constants.SET_PASSWORD_TOKEN_EXPIRES)
        data = {
            'mobile': self.mobile
        }
        token = serializer.dumps(data)  # dumps返回的是byte类型，需要decode一下
        return token.decode()

    @staticmethod
    def check_sms_access_token(access_token):
        serializer = TJSerializer(secret_key=settings.SECRET_KEY, expires_in=constants.SET_PASSWORD_TOKEN_EXPIRES)
        try:
            data = serializer.load(access_token)
        except BadData:
            return None
        else:
            mobile = data.get('mobile')
            return mobile

    def generate_email_verify_url(self):
        serializer = TJSerializer(secret_key=settings.SECRET_KEY, expires_in=constants.EMAIL_VERIFY_TOKEN_EXPIRES)
        data = {
            'user_id': self.id,
            'email': self.email
        }
        token = serializer.dumps(data)
        verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token=' + token.decode()
        return verify_url

    @staticmethod
    def check_email_verify_token(token):
        serializer = TJSerializer(secret_key=settings.SECRET_KEY, expires_in=constants.EMAIL_VERIFY_TOKEN_EXPIRES)
        try:
            data = serializer.loads(token)
        except BadData:
            return False
        else:
            email = data.get('email')
            user_id = data.get('user_id')
            # 查询用户并更新字段的两种方式
            # user = User.objects.get(id=user_id, email=email)
            # user.email_active = True
            # user.save()
            User.objects.filter(id=user_id, email=email).update(email_active=True)
            return True
