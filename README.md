# 🧠 GIFPT AI Worker (Django + Celery)

이 서버는 **GIFPT 프로젝트의 AI 분석 워커(AI Worker)** 로,  
스프링 백엔드(GIFPT-BE)에서 업로드된 PDF와 사용자 프롬프트를 받아  
비동기적으로 AI 모델(GPT 등)을 호출하고, 분석 결과를 반환하거나 콜백으로 통보하는 역할을 합니다.

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
   - Redis를 브로커/백엔드로 사용 (`redis://localhost:6379/0`)
   - 현재는 **GPT 호출을 더미로 사용 중**이며, 이후 자체 모델로 대체 예정
   - 분석 결과를 JSON 형태로 반환:
     ```json
     {
       "summary": "요약 결과 내용...",
       "tokens_used": 2048
     }
     ```

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
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=YOUR_OPENAI_KEY
SPRING_CALLBACK_BASE=http://localhost:8080
```

3.	Django 서버 실행
```
python manage.py runserver 0.0.0.0:8001
```

4.	Celery 워커 실행
```
celery -A gifpt_worker worker -l info
```
