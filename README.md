# 🧠 GIFPT AI Worker (Django + Celery)

이 서버는 **GIFPT 프로젝트의 AI 생성 서버**로,  
사용자가 업로드한 **PDF 자료와 프롬프트(prompt)** 를 기반으로  
우리 팀이 개발한 **AI 모델을 통해 GIF/MP4 애니메이션을 생성하고**,  
생성된 콘텐츠에 대해 **대화형 챗봇으로 추가 설명을 제공**하는 역할을 수행합니다.

---

## 🚀 주요 역할

1. **스프링 백엔드로부터 분석 요청 수신**
   - 엔드포인트: `POST /analyze`
   - 요청 바디 예시:
     ```json
     {
       "job_id": "123",
       "file_path": "uploads/1762415051937_5주차과제.pdf",
       "prompt": "이 PDF의 주요 내용을 요약해줘"
     }
     ```
   - 요청을 Celery 큐에 비동기 작업으로 등록합니다.

2. **Celery 워커를 통해 AI 분석 수행**
   - Celery Worker가 `studio/tasks.py`의 `process_pdf_task()`를 실행합니다.
   - 현재는 **OpenAI GPT 기반 더미 분석 로직**으로 구현되어 있으며,
     차후 실제 GIF/MP4 생성 모델 코드로 교체 예정입니다.

3. **Spring 서버로 완료 콜백 (선택적)**
   - `.env`의 `SPRING_CALLBACK_BASE` 가 설정되어 있으면,
     작업 완료 시 `POST {SPRING_CALLBACK_BASE}/api/v1/analysis/{jobId}/complete` 로 결과를 통보합니다.
   - 실패 시에도 `status: FAILED` 형태로 콜백을 전송합니다.

---

## ⚙️ 기술 스택

| 구성 요소 | 역할 |
|------------|------|
| **Django + DRF** | HTTP API 서버 (`/analyze`) |
| **Celery** | 비동기 태스크 큐 처리 |
| **Redis** | Celery 브로커 및 결과 백엔드 |
| **OpenAI SDK** | GPT 기반 더미 분석 호출 |
| **python-dotenv** | 환경 변수 관리 |
| **requests** | 스프링 콜백 요청 전송 |
| **Flower** | Celery 작업 상태 모니터링 대시보드 |

---

## 🧩 실행 순서

1. Redis 실행  
```bash
docker run -p 6379:6379 redis:7
```

2.	환경 파일 준비
```
python -m venv myvenv
source myvenv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

3.	Django 서버 실행
```
python manage.py migrate
python manage.py runserver
```

4.	Celery 워커 실행
```
celery -A gifpt_worker worker --loglevel=info
```
