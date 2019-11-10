from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from fdfs_client.client import Fdfs_client

import django.views.generic.base.View


@deconstructible
class FastDFSStorage(Storage):

    def __init__(self, conf):
        if conf is None:
            # self.client_conf =
            pass
        self.client_conf = conf

    def _open(self, name, mode='rb'):
        pass

    def _save(self, name, context):
        """
        保存文件
        :param name: 文件名
        :param context:  文件数据
        :return: 存储到数据库中的文件名
        """
        client = Fdfs_client(self.client_conf)

        pass

    def path(self, name):
        pass

    def delete(self, name):
        pass

    def exists(self, name):
        pass

    def listdir(self, path):
        pass

    def size(self, name):
        pass

    def url(self, name):
        pass
