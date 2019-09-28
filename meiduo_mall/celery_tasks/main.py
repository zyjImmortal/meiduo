from celery import Celery
import os

# 导入Django配置文件，celery在获取Django配置文件的时候，是直接向操作系统获取，所以我们需要把
# Django的配置模块加入到环境变量中去
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.dev'

celery_app = Celery("meiduo")

# 导入celery配置文件
celery_app.config_from_object("celery_tasks.config")

# 注册任务,自动扫描任务文件夹下的tasks.py文件里的任务代码
celery_app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.emails'])
# celery_app.register_task(['celery_tasks.email'])

# 开启celery
# celery -A 应用路径(.包路径,里的起始文件) worker -l(指定消息级别) info,
# celery -A celery_tasks.main worker -l info
