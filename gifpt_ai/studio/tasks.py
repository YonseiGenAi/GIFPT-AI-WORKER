# studio/tasks.py

# 실제 우리 ai 모델이 호출될 파일!
import time
from celery import shared_task
from django.core.files.base import ContentFile
from .models import StudioTask

@shared_task
def process_pdf_task(task_id):
    task = StudioTask.objects.get(id=task_id)
    task.status = "processing"
    task.save()

    # 여기에 실제 모델 inference 로직을 넣을 예정
    time.sleep(5)  # 더미 처리 대기
    result_content = f"Processed result for prompt: {task.prompt}".encode("utf-8")

    task.result_file.save(f"result_{task.id}.txt", ContentFile(result_content))
    task.status = "completed"
    task.save()

    return f"Task {task_id} completed"
