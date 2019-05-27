from celery import Celery
# 导入异步模块
from django.core.mail import send_mail
from dailyfresh.settings import EMAIL_FROM
import os
from celery import Celery, platforms
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailyfresh.settings')



app = Celery('celery_tasks.tasks',broker='redis://localhost:6379/0')
# 建立异步对象 参数一:默认路径  参数2：redis进场 8号数据库

# 发邮件 :任务函数，  对象.tasks装饰
@app.task
def send_active_mail(email,token,user_name):
    title = '邮件激活'
    sender = EMAIL_FROM
    receiver = [email]
    html_message = '<h1>%s,你的激活邮件</h1></br><p>请点击链接</p><a href="127.0.0.1:8000/user/active/%s">127.0.0.1:8000/user/active/%s</a>'%(user_name,token,token)
    send_mail(title,'',sender,receiver,html_message=html_message)