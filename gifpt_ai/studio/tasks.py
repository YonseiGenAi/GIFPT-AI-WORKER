# studio/tasks.py

# 실제 우리 ai 모델이 호출될 파일!
import os
import time
from celery import shared_task
from django.core.files.base import ContentFile
from .models import StudioTask
import requests

SPRING_BASE = os.getenv("SPRING_CALLBACK_BASE", "http://localhost:8080")


@shared_task(bind=True)
def process_pdf_task(self, job_id: int, pdf_path: str, prompt: str):
    try:
        # 1) (선택) 스프링에 RUNNING 표시 원하면 별도 엔드포인트 만들어 호출해도 됨
        # requests.post(f"{SPRING_BASE}/api/v1/analysis/{job_id}/running", timeout=5)

        # 2) 실제 처리 로직 (여긴 더미)
        # ... PDF 파싱/모델생성 ...
        result_url = f"http://localhost:8000/static/results/{job_id}.mp4"
        summary = f"요약: '{prompt}'에 따라 생성한 결과입니다."

        # 3) 성공 콜백
        payload = {
            "status": "SUCCESS",
            "resultUrl": result_url,
            "summary": summary,
            "errorMessage": None
        }
        requests.post(
            f"{SPRING_BASE}/api/v1/analysis/{job_id}/complete",
            json=payload, timeout=10
        )
    except Exception as e:
        # 4) 실패 콜백
        payload = {
            "status": "FAILED",
            "resultUrl": None,
            "summary": None,
            "errorMessage": str(e)
        }
        try:
            requests.post(
                f"{SPRING_BASE}/api/v1/analysis/{job_id}/complete",
                json=payload, timeout=10
            )
        except Exception:
            pass
        raise
