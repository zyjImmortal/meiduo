
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from .models import Area
from . import serializers


# Create your views here.

class AreasViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    # queryset = Area.objects.all() 在使用查询集的时候，需要加入过滤条件，
    # 需要自定义获取方法
    # CacheResponseMixin提供缓存支持

    # 分页的量两种开启方式，
    #   1、在配置文件中  是针对全局的
    #   2、在类视图中，只针对当前视图
    pagination_class = None  # 关闭分页

    def get_queryset(self):
        if self.action == 'list':
            return Area.objects.filter(parent=None)
        else:
            return Area.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.AreaSerializer
        else:
            return serializers.SubAreaSerializer
