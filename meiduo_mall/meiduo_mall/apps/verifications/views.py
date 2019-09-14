from django.http import HttpResponse

# Create your views here.
from django_redis import get_redis_connection
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from meiduo_mall.libs.captcha.captcha import captcha
from meiduo_mall.libs.yuntongxun.sms import CCP

from verifications.serializers import CheckImageCodeSerializer
from . import constants

import random


class ImageCodeView(APIView):
    """
    图片验证码
    image_code_id路径参数
    """

    def get(self, request, image_code_id: int) -> HttpResponse:
        # 生成验证码
        text, image = captcha.generate_captcha()
        # 获取Redis链接，并将生成的验证码存入Redis
        redis_conn = get_redis_connection("verify_codes")
        redis_conn.setex("img_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
        return HttpResponse(image, content_type="image/jpg")


class SMSCodeView(GenericAPIView):
    serializer_class = CheckImageCodeSerializer

    def get(self, request, mobile):
        serializer = self.get_serializer()
        serializer.is_valid(raise_exception=True)

        sms_code = '%06d' % random.randint(0, 999999)
        redis_conn = get_redis_connection("verify_codes")
        # redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRE, sms_code)
        # redis_conn.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        # 获取管道
        pipeline = redis_conn.pipeline()
        # 收集命令
        pipeline.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRE, sms_code)
        pipeline.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        # 提交执行
        pipeline.execute()
        # 使用Redis的pipeline管道,一次处理多e个命令
        ccp = CCP()
        time = str(constants.SMS_CODE_REDIS_EXPIRE / 60)
        ccp.send_template_sms(mobile, [sms_code, time], constants.SMS_CODE_TEMPLATE_ID)

        return Response({"message": "ok"})
