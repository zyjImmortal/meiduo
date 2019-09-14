from django_redis import get_redis_connection
from redis import RedisError
from rest_framework import serializers
import logging

logger = logging.getLogger("django")


# 模型序列化器，序列化器中的字段对应数据库中的字段，进行校验
# 根本序列化器
class CheckImageCodeSerializer(serializers.Serializer):
    """图片验证码校验序列化器"""

    # mobile 通过路由的正则表达式来匹配同时也可以校验
    image_code_id = serializers.UUIDField()
    text = serializers.CharField(min_length=4, max_length=4)

    # 带下划线只针对某个字段，不带下划线针对所有字段

    def validate(self, attrs: dict):
        """校验图片验证码"""
        redis_conn = get_redis_connection("verify_codes")
        real_image_code = redis_conn.get("img_%s" % attrs['image_code_id'])
        if real_image_code is None:
            # 序列化器中是直接返回异常
            raise serializers.ValidationError("无效的图片验证码")
        real_image_code = real_image_code.decode()
        # 删除图片验证码,捕获一下异常，但是不抛出，以免影响下面发送验证码
        # 如果发生异常，错误处理器会统一捕获并返回错误给前端，就不往下走发送验证码的代码，但是此处却没必要返回
        try:
            redis_conn.delete("img_%s" % attrs['image_code_id'])
        except RedisError as e:
            logger.error(e)

        if real_image_code.lower() != attrs['text'].lower():
            raise serializers.ValidationError("图片验证码错误")
        mobile = self.context['view'].kwargs['mobile']
        send_flag = redis_conn.get("send_flag_%s" % mobile)
        if send_flag:
            raise serializers.ValidationError("发送短信验证码过于频繁,请稍后再试")
        return attrs

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
