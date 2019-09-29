from celery_tasks.main import celery_app
from django.core.mail import send_mail
from django.conf import settings


@celery_app.task(name='send_verify_email')
def send_verify_email(to_email, verify_url):
    """
    发送验证邮件
    :param to_email:  收件人
    :param verify_url:激活链接
    :return: None
    """
    subject = '美多商城邮箱验证码'
    # 也可以使用str.format(ket=value)这种形式格式化
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%(email)s。请点此链接激活您的邮箱：</p>' \
                   '<p><a href="%(verify_url)s">%(verify_url)s</a></p>' % {'email': to_email, 'verify_url': verify_url}

    send_mail(subject, "", settings.EMAIL_FROM, [to_email], html_message=html_message)
