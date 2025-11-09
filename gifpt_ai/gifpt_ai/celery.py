# gifpt_ai/celery.py
import os
from celery import Celery

# Django 설정 모듈 지정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gifpt_ai.settings')

# Celery 앱 생성
app = Celery('gifpt_ai')

# Django의 settings.py에서 CELERY 관련 설정 자동 로드
app.config_from_object('django.conf:settings', namespace='CELERY')

# 모든 app 폴더에서 tasks.py 자동 탐색
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
