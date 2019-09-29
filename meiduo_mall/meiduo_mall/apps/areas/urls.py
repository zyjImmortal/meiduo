from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include
from . import views

router = DefaultRouter()
router.register('areas', views.AreasViewSet, base_name='area')
router.register('address', views.AddressViewSet, base_name='address')
urlpatterns = [
    # url('', include(router.urls))  和下面的注册url方式一样的效果
]

urlpatterns += router.urls
