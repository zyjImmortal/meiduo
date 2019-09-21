from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    """
    扩展django自带的用户模型，增加phone字段,使用Django提供的认证系统
    """
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号")

    class Meta:
        db_table = 'tb_users'
        verbose_name = "用户"  # 指明一个易于理解和表述的对象名称，单数形式
        verbose_name_plural = verbose_name  # 复数形式
