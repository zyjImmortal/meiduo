from celery import Celery

celery_app = Celery("meiduo")

# 导入配置文件
celery_app.config_from_object("celery_tasks.config")

# 注册任务,自动扫描任务文件夹下的tasks.py文件里的任务代码
celery_app.autodiscover_tasks(['celery_tasks.sms'])

# 开启celery
# celery -A 应用路径(.包路径,里的起始文件) worker -l(指定消息级别) info,
# celery -A celery_tasks.main worker -l info
