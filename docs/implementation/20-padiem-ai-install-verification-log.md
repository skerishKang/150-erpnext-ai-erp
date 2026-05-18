# 20 - Padiem AI Install Verification Log

| 항목 | 내용 |
|------|------|
| 문서 버전 | v1.0 |
| 작성일 | 2026-05-18 |
| Issue | #21 |
| PR | test/issue-21-padiem-ai-install-verification |
| 상태 | 검증 성공 |

---

## 1. 작업 목적

PR #20과 PR #22로 main에 들어간 `padiem_ai` app skeleton + provider registry가 로컬 ERPNext Docker lab 안에서 실제로 import/install 가능한지 검증합니다.

---

## 2. Docker 환경

### Docker Desktop 상태

| 항목 | 값 |
|------|-----|
| Docker Desktop | 실행됨 |
| Docker Engine | 정상 |
| 컨테이너 시작 | `docker compose -f pwd.yml up -d` |

### 컨테이너 상태

| 컨테이너 | 상태 |
|----------|------|
| frappe_docker-frontend-1 | Up (nginx) |
| frappe_docker-backend-1 | Up (gunicorn) |
| frappe_docker-websocket-1 | Up |
| frappe_docker-scheduler-1 | Up |
| frappe_docker-queue-long-1 | Up |
| frappe_docker-queue-short-1 | Up |
| frappe_docker-redis-cache-1 | Up |
| frappe_docker-redis-queue-1 | Up |
| frappe_docker-db-1 | Up (healthy) |

---

## 3. bench 실행 컨테이너

| 항목 | 값 |
|------|-----|
| bench 실행 컨테이너 | `backend` (frappe_docker-backend-1) |
| bench 버전 | Frappe 16.18.1, ERPNext 16.18.3 |
| site 이름 | `frontend` |

---

## 4. padiem_ai App 반영

### 반영 방식

| 단계 | 명령 | 결과 |
|------|------|------|
| 1. app 복사 | `docker cp padiem_ai frappe_docker-backend-1:/home/frappe/frappe-bench/apps/padiem_ai` | 성공 |
| 2. 권한 수정 | `chown -R frappe:frappe apps/padiem_ai` | 성공 |
| 3. .pth 파일 생성 | `echo '/home/frappe/frappe-bench/apps/padiem_ai' > env/lib/python3.14/site-packages/padiem_ai.pth` | 성공 |
| 4. apps.txt 등록 | `echo 'padiem_ai' >> sites/apps.txt` | 성공 |
| 5. apps.json 업데이트 | padiem_ai 엔트리 추가 | 성공 |
| 6. hooks.py 위치 수정 | `padiem_ai/hooks.py` → `padiem_ai/padiem_ai/hooks.py` (Frappe 표준 구조) | 성공 |
| 7. frontend 컨테이너에도 반영 | 동일한 복사 + .pth + 권한 수정 | 성공 |
| 8. 컨테이너 재시작 | `docker compose restart backend` | 성공 |

### 수정된 파일 구조

```
padiem_ai/                    ← 앱 루트 (setup.py, README.md)
└── padiem_ai/                ← Python 패키지 (__init__.py, hooks.py)
    ├── hooks.py              ← Frappe hooks (Frappe 표준 위치)
    ├── modules.txt           ← 모듈 정의
    ├── patches.txt           ← 패치 정의 (빈 파일)
    ├── ai/                   ← AI provider abstraction
    ├── api/                  ← API endpoints
    └── ...
```

### 발생한 오류와 해결

| 오류 | 원인 | 해결 |
|------|------|------|
| `No module named 'padiem_ai'` | `.pth` 파일 미생성 | virtualenv site-packages에 `.pth` 파일 생성 |
| `Permission denied` | Docker cp 후 소유권 문제 | `chown -R frappe:frappe` 적용 |
| `No module named 'padiem_ai.hooks'` | hooks.py 위치 불일치 | `padiem_ai/hooks.py` → `padiem_ai/padiem_ai/hooks.py` 이동 |
| 500 에러 (Desk) | frontend 컨테이너에 app 미반영 | frontend에도 app 복사 + .pth 생성 |
| 500 에러 지속 | backend 컨테이너 재시작 필요 | `docker compose restart backend` |

---

## 5. install-app 결과

```
$ bench --site frontend install-app padiem_ai
Installing padiem_ai...
Creating Workspace Sidebars
Creating Desktop Icons
Updating Dashboard for padiem_ai
```

**결과**: 성공

---

## 6. Python Import 테스트

### Docker 내부 import 테스트

```
$ python -c "from padiem_ai.ai.registry import list_providers, get_provider; ..."

list_providers: ['mock', 'kilocode', 'opencodego', 'nvidia', 'deepseek', 'mistral', 'ollama']
count: 7
mock: {'status': 'ok', 'provider': 'mock', 'latency_ms': 0}
kilocode: {'status': 'not_implemented', 'provider': 'kilocode', 'message': "Provider 'kilocode' is registered but not yet implemented."}
ALL TESTS PASSED
```

### ProviderRegistry Docker 내부 테스트

| 테스트 | 결과 |
|--------|------|
| `list_providers()` | 7개 provider 반환 |
| `get_provider('mock').health_check()` | `{'status': 'ok', 'provider': 'mock', 'latency_ms': 0}` |
| `get_provider('kilocode').health_check()` | `{'status': 'not_implemented', ...}` |
| 외부 API 호출 | 없음 |

---

## 7. Desk 접속 확인

| 항목 | 값 |
|------|-----|
| URL | http://localhost:8080/desk |
| HTTP 상태 | 200 |
| fatal error | 없음 |

---

## 8. API Method Path 확인

| 항목 | 값 |
|------|-----|
| Method path | `padiem_ai.api.briefing.get_ceo_briefing` |
| HTTP 응답 | 인증 필요 (PermissionError) — 정상 동작 |
| path 해석 | Frappe가 method path를 정상 인식 |

**참고**: 403/PermissionError는 인증 문제이지, method path 실패가 아닙니다.

---

## 9. 외부 API 호출 / Credential

| 항목 | 값 |
|------|-----|
| 외부 AI API 호출 | 없음 |
| KiloCode/OpenCodeGo/Nvidia/DeepSeek 호출 | 없음 |
| API key | 없음 |
| Credential | 없음 |
| Docker volume 삭제 | 없음 |

---

## 10. #18/#21 Close 판단

| 기준 | 상태 |
|------|------|
| `bench new-app padiem_ai` | 수동 생성으로 대체 (Docker 내부 bench에서 검증) |
| `bench --site frontend install-app padiem_ai` | **성공** |
| App file structure matches strategy document | **확인** |
| Implementation log created | **확인** |
| No credentials in committed files | **확인** |
| Desk fatal error 없음 | **확인** |
| Provider registry Docker 내부 동작 | **확인** |

**판정**: #18과 #21 close 가능.

---

**문서 버전**: v1.0
**작성일**: 2026-05-18
**상태**: 검증 성공 — #18, #21 close 대상
