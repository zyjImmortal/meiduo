from rest_framework import serializers
from django_redis import get_redis_connection
import re

from rest_framework_jwt.settings import api_settings

from users.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(label="确认密码", required=True,
                                             allow_null=False, allow_blank=False, write_only=True)
    sms_code = serializers.CharField(label="验证码", required=True, allow_null=False,
                                     allow_blank=False, write_only=True)
    allow = serializers.CharField(label="同意协议", required=True, allow_null=False,
                                  allow_blank=False, write_only=True)
    token = serializers.CharField(label='登录状态token', read_only=True)  # 增加token字段

    def validate_mobile(self, value):
        if not re.match(r'1[3-9]\d{9}$', value):
            raise serializers.ValidationError("手机号格式错误")

    def validate_allow(self, value):
        if value != 'true':
            raise serializers.ValidationError("请同意用户协议")

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("两次密码不一致")
        redis_conn = get_redis_connection("verify_codes")
        mobile = attrs['mobile']
        real_sms_code = redis_conn.get("sms_%s" % mobile)
        if not real_sms_code:
            raise serializers.ValidationError("验证码已过期")
        if real_sms_code.decode() != attrs['sms_code']:
            raise serializers.ValidationError("输入的验证码错误")
        return attrs

    def create(self, validated_data):
        # 移除数据库不存在的属性
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']
        user = super().create(validated_data)
        user.set_password(validated_data['password'])

        # 补充生成记录登录状态的token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2', 'sms_code', 'mobile', 'allow', 'token')
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }
