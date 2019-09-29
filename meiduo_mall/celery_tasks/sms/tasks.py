from celery_tasks.main import celery_app
from .yuntongxun.sms import CCP
from . import constants


@celery_app.task(name="send_sms")  # 标记为一个异步任务
def send_sms(mobile, sms_code):
    """
    发送短信任务
    :param mobile: 手机号
    :param sms_code: 验证码
    :return: None
    """

    ccp = CCP()
    time = str(constants.SMS_CODE_REDIS_EXPIRE / 60)
    ccp.send_template_sms(mobile, [sms_code, time], constants.SMS_CODE_TEMPLATE_ID)
