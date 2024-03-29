from rest_framework import serializers

from areas.models import Area
from users.models import Address


class AreaSerializer(serializers.ModelSerializer):
    """行政区域序列化器"""

    class Meta:
        model = Area
        fields = ('id', 'name')


class SubAreaSerializer(serializers.ModelSerializer):
    """子级区域序列化器"""

    subs = AreaSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        # 在模型中定义了related_name='subs'才可以使用
        fields = ('id', 'name', 'subs')


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('receiver', 'title', 'province', 'city', 'district', 'place', 'mobile', 'tel', 'email')
