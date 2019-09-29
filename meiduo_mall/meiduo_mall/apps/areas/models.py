from django.db import models


# Create your models here.

class Area(models.Model):
    """
    行政区划
    """
    name = models.CharField(max_length=20, verbose_name='名称')
    #
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True, blank=True,
                               verbose_name='上级行政区划')

    class Meta:
        db_table = 'tb_areas'
        verbose_name = '行政区划'
        verbose_name_plural = '行政区划'

    def __str__(self):
        return self.name

# 在一对多的时候，在获取多的时候(也就是子集的时候，Django默认使用的方式,类型_set)
# 也可以模型中通过指定related_name属性，在查询的时候使用area1.related_name获取所有子集数据


