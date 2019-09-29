from django.contrib.auth.backends import ModelBackend

from users.models import User
import re


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功的返回数据
    :param token:
    :param user:
    :param request:
    :return:
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


def get_user_by_account(account):
    """
    根据账号信息查找用户
    :param account: 账号可能是用户名或者手机号
    :return:
    """
    try:
        if re.match(r'1[3-9]\d{9}', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except User.DoseNotExist:
        return None
    return user


class UsernameMobileAuthBackend(ModelBackend):
    """
    自定义认证方法，
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)
        if user is not None and user.check_password(password):
            return user
