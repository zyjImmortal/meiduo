from django.conf.urls import url

from verifications import views

urlpatterns = [
    url(r'image_code/(?P<image_code_id>.+)', views.ImageCodeView.as_view()),
    url(r'sms_codes/(?P<mobile>1[3-9]\d{9})', views.SMSCodeView.as_view()),
    url(r'/sms_codes', views.SmsCodeByTokenView.as_view())
]
