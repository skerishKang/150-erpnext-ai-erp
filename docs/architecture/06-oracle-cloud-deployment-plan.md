# Oracle Cloud 배포 계획: Padiem AI ERP v1

| 항목 | 내용 |
|------|------|
| 문서 버전 | v1.0 |
| 작성일 | 2026-05-18 |
| 대상 | Padiem AI ERP 첫 파일럿 배포 |
| 상태 | Draft |

---

## 1. 배포 목적

### 이 문서가 왜 필요한가

Padiem AI ERP는 로컬 Docker 환경에서 ERPNext를 검증했습니다. 이제 이 환경을 Oracle Cloud VM으로 옮겨야 합니다. 그래야 파일럿 고객이 브라우저에서 접속할 수 있습니다.

이카운트처럼 고객이 소프트웨어를 설치하지 않고, 브라우저에 URL만 입력하면 ERP를 쓸 수 있는 구조를 목표로 합니다.

### 핵심 목표

| 목표 | 설명 |
|------|------|
| **Cloud ERP 제공** | 브라우저 기반 클라우드 ERP 형태로 파일럿 고객에게 제공 |
| **로컬 → 클라우드 이전** | Docker 기반 ERPNext 환경을 Oracle Cloud VM으로 이동 |
| **설치 없는 접속** | 고객이 브라우저만으로 ERP 접속 가능 |
| **안전한 파일럿** | 고객 데이터 보호, 백업/복원 가능 |

### 명시적 제외

**이 문서는 실제 배포가 아니라 배포 계획입니다.**

이 문서에서 하지 않는 것:
- Oracle Cloud VM 생성
- 실제 도메인 설정
- 실제 SSL 발급
- 실제 credential 기록
- Docker 컨테이너 실행
- 고객 데이터 사용

---

## 2. 배포 원칙

### 기본 원칙

| 원칙 | 설명 |
|------|------|
| **Cloud-first** | 클라우드 배포를 기본으로 고려 |
| **Docker 기반** | Docker Compose 기반 배포 |
| **ERPNext core 미수정** | ERPNext 표준 코드를 직접 수정하지 않음 |
| **Custom App 구조** | `padiem_ai` Custom App 추가 가능 구조 유지 |
| **고객 데이터 보호** | 고객 데이터 보호를 최우선으로 고려 |
| **백업/복원 가능** | 백업과 복원이 언제든 가능하도록 설계 |
| **단순한 시작** | 초기 파일럿은 단일 VM으로 단순하게 시작 |
| **확장 가능** | 운영 확장 시 staging/production 분리 가능 |

### 파일럿 vs 정식 운영

| 구분 | 파일럿 | 정식 운영 |
|------|--------|----------|
| VM | 단일 VM | 다중 VM / DB 분리 |
| 환경 | local → cloud pilot | staging → production |
| 데이터 | 데모 데이터 또는 제한적 고객 데이터 | 실제 고객 데이터 |
| 백업 | 매일 1회 | 자동화 + 보존 정책 |
| 모니터링 | 기본 상태 확인 | 전체 모니터링 + 알림 |
| SSL | Let's Encrypt 또는 Cloudflare | 동일 |

---

## 3. 권장 초기 아키텍처

### 아키텍처 다이어그램

```
┌──────────────────────────────────────────────────────────────────┐
│                        사용자 브라우저                            │
│                  https://erp.padiem.co.kr                        │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                    Domain / DNS                                   │
│              (A record → Oracle Cloud VM IP)                      │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                    Oracle Cloud VM                                │
│              Ubuntu 24.04 LTS (ARM, 4 OCPU, 16GB+)               │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                  Docker Compose Stack                       │  │
│  │                                                            │  │
│  │  ┌──────────────┐                                          │  │
│  │  │ Nginx        │  ← Reverse proxy, SSL termination        │  │
│  │  │ (port 80/443)│                                          │  │
│  │  └──────┬───────┘                                          │  │
│  │         │                                                  │  │
│  │  ┌──────▼───────┐                                          │  │
│  │  │ ERPNext      │  ← Frappe + ERPNext web                  │  │
│  │  │ Frontend     │     (port 8080)                           │  │
│  │  └──────┬───────┘                                          │  │
│  │         │                                                  │  │
│  │  ┌──────▼───────┐  ┌──────────────┐  ┌──────────────┐     │  │
│  │  │ Backend      │  │ MariaDB      │  │ Redis        │     │  │
│  │  │ (workers)    │  │ (database)   │  │ (cache/queue)│     │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘     │  │
│  │                                                            │  │
│  │  ┌──────────────────────────────────────────────────────┐  │  │
│  │  │ Volumes: sites, db-data, redis-data, logs            │  │  │
│  │  └──────────────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ Backup Storage                                              │  │
│  │ - VM 내부: /mnt/backups/ (임시)                              │  │
│  │ - Oracle Object Storage (권장)                              │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Ports: 22 (SSH), 80 (HTTP), 443 (HTTPS)                        │
└──────────────────────────────────────────────────────────────────┘
                           │
                           ▼ (optional)
┌──────────────────────────────────────────────────────────────────┐
│                AI Provider (외부)                                  │
│           DeepSeek / OpenAI-compatible API                        │
│           관리자 설정 후 활성화                                     │
└──────────────────────────────────────────────────────────────────┘
```

### 데이터 흐름

```
사용자 → Domain → Nginx (SSL) → ERPNext Frontend → Backend → MariaDB
                                                         → Redis
                                                         → AI Provider (optional)
```

---

## 4. Oracle Cloud VM 요구사항

### VM 사양 비교

| 항목 | 최소 사양 (파일럿) | 권장 사양 (운영) |
|------|-------------------|-----------------|
| **Shape** | VM.Standard.A1.Flex | VM.Standard.A1.Flex |
| **OCPU** | 2 | 4 이상 |
| **RAM** | 8 GB | 16 GB 이상 |
| **Boot Storage** | 100 GB | 200 GB |
| **Block Storage** | 없음 (boot만 사용) | 100 GB (DB 전용) |
| **OS** | Ubuntu 24.04 LTS | Ubuntu 24.04 LTS |
| **Network** | Public IP 1개 | Public IP 1개 (고정 IP 권장) |
| **Bandwidth** | 10 TB/월 (무료 포함) | 10 TB/월 |

### 필수 소프트웨어

| 소프트웨어 | 버전 | 설명 |
|-----------|------|------|
| Docker | 최신 stable | 컨테이너 런타임 |
| Docker Compose | v2.x | 멀티 컨테이너 오케스트레이션 |
| Git | 최신 stable | 코드 관리 |
| curl | 기본 포함 | API 테스트 |
| ufw | 기본 포함 | 방화벽 관리 |

### 네트워크 포트

| 포트 | 프로토콜 | 용도 | 외부 노출 |
|------|---------|------|----------|
| 22 | TCP | SSH 접속 | 예 (key 기반) |
| 80 | TCP | HTTP (→ HTTPS 리다이렉트) | 예 |
| 443 | TCP | HTTPS | 예 |
| 8080 | TCP | ERPNext Frontend | 아니오 (Nginx에서 프록시) |
| 3306 | TCP | MariaDB | 아니오 (Docker 내부) |
| 6379 | TCP | Redis | 아니오 (Docker 내부) |

### 보안 그룹 / 방화벽

```
Ingress:
  - 22/tcp: SSH (IP 제한 권장)
  - 80/tcp: HTTP (모든 IP)
  - 443/tcp: HTTPS (모든 IP)

Egress:
  - 모든 outbound 허용 (AI provider API 호출 등 필요)
```

### SSH 접근 방식

- SSH key 기반 접속만 허용
- Password 로그인 비활성화
- root 로그인 비활성화
- 별도 admin 사용자 생성

---

## 5. Docker 배포 구조

### 현재 로컬 환경

현재 로컬에서는 `frappe_docker` 기반으로 ERPNext를 구동하고 있습니다.

```
로컬 환경:
  - frappe_docker 프로젝트 기반
  - docker compose로 컨테이너 실행
  - pwd.yml 또는 custom compose 파일 사용
  - site 이름: frontend
```

### 클라우드 배포 방식

클라우드에서도 `frappe_docker` 또는 공식 권장 Docker 배포 방식을 검토합니다.

| 방식 | 설명 | 장점 | 단점 |
|------|------|------|------|
| **frappe_docker** | 공식 frappe_docker 프로젝트 | 검증됨, 커뮤니티 지원 | compose 파일 커스터마이즈 필요 |
| **Custom compose** | 프로젝트에 맞게 compose 파일 작성 | 완전한 제어 | 직접 관리 필요 |

### Production compose 구성 검토

운영 환경에서는 `pwd.yml` 그대로 사용하지 않고, production compose 구성을 검토해야 합니다.

| 항목 | pwd.yml (현재) | Production (권장) |
|------|----------------|------------------|
| **Nginx** | 포함 안 됨 | Reverse proxy 포함 |
| **SSL** | 없음 | SSL termination 포함 |
| **볼륨** | 기본 | Named volume, 외부 마운트 |
| **로그** | 기본 | 로그 수집 설정 |
| **재시작 정책** | 기본 | `restart: always` |
| **헬스체크** | 기본 | Health check 설정 |
| **리소스 제한** | 없음 | CPU/Memory 제한 |

### Volume 보존 원칙

| 원칙 | 설명 |
|------|------|
| **down -v 금지** | `docker compose down -v`로 volume 삭제하지 않음 |
| **Named volume 사용** | 모든 데이터는 named volume에 저장 |
| **외부 마운트 권장** | 중요 데이터는 host 경로에 마운트 |
| **백업 전 down 금지** | 백업 없이 컨테이너 중지하지 않음 |

---

## 6. 도메인/SSL 계획

### 도메인 전략

| 구분 | 도메인 | 시점 |
|------|--------|------|
| **초기 파일럿** | IP 직접 접속 또는 임시 서브도메인 | Phase 1 |
| **정식 파일럿** | `erp.padiem.co.kr` 또는 고객 도메인 | Phase 2 |
| **고객별** | `ai-erp.customer-domain.com` | Phase 3 |

> **주의**: `erp.padiem.co.kr`, `ai-erp.customer-domain.com`은 예시입니다. 실제 도메인 구매/설정은 별도 작업입니다.

### SSL 전략

| 방식 | 설명 | 시점 |
|------|------|------|
| **Let's Encrypt** | 무료 SSL 인증서, 자동 갱신 | Phase 1 권장 |
| **Cloudflare** | CDN + SSL + DDoS 보호 | Phase 2 검토 |
| **Self-signed** | 개발/테스트용 | 개발 환경에서만 |

### SSL 적용 방식

```
방식 1: Nginx + Let's Encrypt (권장)
  - Nginx가 SSL termination 담당
  - certbot으로 인증서 발급/갱신
  - 90일마다 자동 갱신

방식 2: Cloudflare (대안)
  - Cloudflare에서 SSL 처리
  - Origin server는 HTTP 또는 Cloudflare origin certificate
  - CDN + 보안 기능 추가
```

---

## 7. 보안 계획

### 필수 보안 조치

| 조치 | 설명 | 우선순위 |
|------|------|---------|
| **Administrator 비밀번호 변경** | 기본 `admin` 비밀번호 즉시 변경 | 즉시 |
| **SSH key 기반 접속** | Password 로그인 비활성화 | 즉시 |
| **root login 제한** | root 직접 접속 비활성화 | 즉시 |
| **방화벽 설정** | 필요한 포트(22, 80, 443)만 허용 | 즉시 |
| **DB 포트 외부 노출 금지** | MariaDB 3306 포트 외부 차단 | 즉시 |
| **Redis 외부 노출 금지** | Redis 6379 포트 외부 차단 | 즉시 |
| **Git 커밋 금지 파일** | site_config, .env, API key, backup 파일 | 즉시 |
| **관리자 계정 최소화** | 불필요한 관리자 계정 삭제 | 정기 |
| **정기 보안 업데이트** | `apt update && apt upgrade` 정기 실행 | 정기 |

### SSH 설정

```bash
# /etc/ssh/sshd_config 권장 설정 (concept only)
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
```

### 방화벽 설정

```bash
# ufw 방화벽 설정 (concept only)
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable
```

### Git 커밋 금지 파일 목록

| 파일/패턴 | 설명 |
|-----------|------|
| `site_config.json` | DB 비밀번호, API key 포함 |
| `.env` | 환경변수, credential 포함 |
| `*.sql.gz` | 데이터베이스 백업 |
| `*.tar.gz` | 파일 백업 |
| `cookies.txt` | 세션 쿠키 |
| `id_rsa`, `*.pem` | SSH 키 |

---

## 8. 백업/복원 계획

### 백업 대상

| 대상 | 방법 | 빈도 | 보존 기간 |
|------|------|------|----------|
| **ERPNext DB** | `bench backup` 또는 `mysqldump` | 매일 1회 | 7일 |
| **Site files** | 파일시스템 백업 | 매일 1회 | 7일 |
| **Docker volume** | volume 스냅샷 | 매주 1회 | 4주 |
| **VM 전체** | OCI boot volume backup | 매주 1회 | 4주 |
| **설정 파일** | Git 저장 | 변경 시 | 영구 |

### 백업 저장 위치

| 위치 | 설명 | 시점 |
|------|------|------|
| **VM 내부** | `/mnt/backups/` (임시) | 파일럿 |
| **Oracle Object Storage** | 장기 저장, 내구성 높음 | 운영 권장 |
| **별도 외부 저장소** | S3 호환 등 | 운영 대안 |

### 백업 커맨드 (concept only)

```bash
# ERPNext DB 백업
docker exec frappe_docker-frontend-1 bench --site frontend backup --compress

# 백업 파일 복사 (VM 내부)
cp /path/to/backups/*.sql.gz /mnt/backups/erpnext/

# Oracle Object Storage 업로드 (concept only)
oci os object put --bucket-name padiem-backups --file backup.sql.gz
```

### 복원 커맨드 (concept only)

```bash
# DB 복원
docker exec frappe_docker-frontend-1 bench --site frontend restore /path/to/backup.sql.gz

# 복원 확인
docker exec frappe_docker-frontend-1 bench --site frontend list-sites
```

### 복원 테스트

**복원 테스트는 반드시 실제 백업으로 정기적으로 수행해야 합니다.**

| 테스트 | 빈도 | 방법 |
|--------|------|------|
| DB 복원 테스트 | 매월 1회 | 별도 환경에서 복원 후 확인 |
| Site files 복원 | 매월 1회 | 파일 복원 후 접속 확인 |
| 전체 VM 복원 | 분기 1회 | OCI backup으로 VM 복원 |

---

## 9. Staging / Production 구분

### 환경 구분

| 구분 | local | cloud pilot | staging | production |
|------|-------|-------------|---------|------------|
| **목적** | 개발/테스트 | 첫 파일럿 | 정식 테스트 | 실제 운영 |
| **데이터** | 데모 데이터 | 데모 또는 제한적 고객 데이터 | 가상 데이터 | 실제 고객 데이터 |
| **접속** | localhost | IP 또는 임시 도메인 | 서브도메인 | 정식 도메인 |
| **SSL** | 없음 | Let's Encrypt | Let's Encrypt | Let's Encrypt / Cloudflare |
| **백업** | 수동 | 매일 1회 | 자동화 | 자동화 + 보존 정책 |
| **AI provider** | Mock | Mock 또는 DeepSeek | Mock 또는 DeepSeek | DeepSeek 등 |

### Staging과 Production 분리 원칙

| 원칙 | 설명 |
|------|------|
| **DB 분리** | staging과 production DB를 완전히 분리 |
| **Volume 분리** | Docker volume을 별도로 관리 |
| **Credential 분리** | AI provider credential도 분리 |
| **네트워크 분리** | 가능하면 별도 VM 또는 별도 Docker stack |

### 초기 파일럿 흐름

```
Phase 1: local (개발)
  └→ 데모 데이터로 기능 검증

Phase 2: cloud pilot (첫 파일럿)
  └→ Oracle Cloud VM에 배포
  └→ 데모 데이터 또는 제한적 고객 데이터
  └→ 단일 VM, 단일 site

Phase 3: staging + production (정식 운영)
  └→ staging: 정식 테스트 환경
  └→ production: 실제 고객 데이터
  └→ VM 분리 또는 site 분리
```

---

## 10. AI Provider 배포 고려사항

### 기본 원칙

| 원칙 | 설명 |
|------|------|
| **기본 mock/local-safe mode** | 개발/파일럿初期에는 MockProvider 사용 |
| **관리자 설정 후 활성화** | 외부 provider는 관리자 설정과 명시적 동의 후 활성화 |
| **Credential Git 금지** | API key는 Git 밖에서 관리 |
| **최소 데이터 전달** | 외부 전송 시 최소 필요 데이터만 전달 |
| **Fallback 준비** | provider timeout/fallback/degraded mode 대비 |

### 클라우드 환경에서의 Credential 관리

```
방식 1: 환경변수 (권장)
  - Docker compose에서 환경변수로 전달
  - .env 파일에 저장 (Git 제외)

방식 2: Frappe site_config
  - sites/frontend/site_config.json에 저장
  - Git 제외

방식 3: 외부 secret manager (운영)
  - Oracle Vault 등 사용
  - 가장 안전하지만 복잡
```

---

## 11. 고객별 배포 전략

### 두 가지 방식 비교

| 항목 | A. 고객별 독립 VM | B. 하나의 VM, 고객별 site 분리 |
|------|------------------|-------------------------------|
| **보안** | 완전 격리 | 논리적 격리 (DB 분리) |
| **비용** | 높음 (VM × 고객 수) | 낮음 (VM 1개 + site 분리) |
| **운영 난이도** | 높음 (각 VM 관리) | 중간 (1개 VM 내 관리) |
| **백업/복원** | 단순 (VM별 독립) | 주의 필요 (site별 분리) |
| **파일럿 적합성** | 안전하지만 비쌈 | 비용 효율적 |

### 초기 추천

| 시점 | 추천 방식 | 이유 |
|------|----------|------|
| **첫 파일럿 (1~2 고객)** | 고객별 독립 VM 또는 독립 site | 안전성 우선 |
| **초기 확장 (3~5 고객)** | 고객별 site 분리 (1 VM) | 비용 절감 |
| **정식 운영 (5+ 고객)** | 고객별 독립 VM 또는 멀티 VM | 보안/안정성 |

### 고객 데이터 분리 원칙

**실제 고객 데이터가 들어가면 고객별 분리가 안전합니다.**

| 원칙 | 설명 |
|------|------|
| **DB 분리** | 고객별로 별도 MariaDB database 사용 |
| **Site 분리** | 고객별로 별도 Frappe site 사용 |
| **Volume 분리** | 고객별로 별도 site files volume 사용 |
| **Credential 분리** | 고객별로 별도 AI provider credential 가능 |

---

## 12. 운영 체크리스트

### 서버 생성 및 초기 설정

- [ ] Oracle Cloud 계정 생성
- [ ] ARM VM 생성 (Ubuntu 24.04 LTS)
- [ ] SSH key 설정
- [ ] 보안 그룹 설정 (22, 80, 443)
- [ ] 시스템 패키지 업데이트
- [ ] Docker 및 Docker Compose 설치

### ERPNext 배포

- [ ] frappe_docker 클론 또는 compose 파일 준비
- [ ] 환경변수 설정 (.env)
- [ ] Docker Compose 실행
- [ ] 모든 컨테이너 healthy 확인
- [ ] ERPNext site 생성
- [ ] Setup Wizard 완료

### 보안 설정

- [ ] Administrator 비밀번호 변경
- [ ] SSH password 로그인 비활성화
- [ ] root 로그인 비활성화
- [ ] 방화벽 설정 확인
- [ ] DB 포트 외부 노출 차단 확인
- [ ] Redis 외부 노출 차단 확인

### 네트워크 및 SSL

- [ ] Public IP 확인 (고정 IP 권장)
- [ ] DNS 설정 (A record)
- [ ] Nginx reverse proxy 설정
- [ ] SSL 인증서 발급 (Let's Encrypt)
- [ ] HTTPS 접속 확인

### 백업 및 모니터링

- [ ] 백업 스케줄 설정 (매일 1회)
- [ ] 백업 저장 위치 확인
- [ ] 복원 테스트 수행
- [ ] 기본 상태 모니터링 설정
- [ ] 디스크 사용량 알림 설정

### 데모 준비

- [ ] 데모 데이터 또는 고객 데이터 입력
- [ ] padiem_ai app 설치 준비
- [ ] AI provider 설정 (Mock 또는 DeepSeek)
- [ ] 테스트 로그인 확인
- [ ] 데모 시나리오 테스트

---

## 13. 비용 고려

### Oracle Cloud 비용 (월간 추정)

| 항목 | 무료 티어 | 유료 (파일럿) |
|------|----------|--------------|
| **VM compute** | 0원 (무료 티어 내) | 30,000~50,000원 |
| **Block storage (100GB)** | 0원 (200GB까지 무료) | ~10,000원 |
| **Bandwidth** | 0원 (10TB/월 무료 포함) | ~0원 (파일럿 트래픽 적음) |
| **Object Storage** | 0원 (20GB 무료) | ~5,000원 |
| **합계** | ~0원 | ~45,000~65,000원 |

> **주의**: 정확한 금액은 리전, 사양, 사용량에 따라 달라집니다.

### 파일럿 가격과 서버비 관계

| 파일럿 가격 | 서버비 (월) | 수익성 |
|------------|-----------|--------|
| 100만~300만원 (첫 레퍼런스) | ~5만원 | 서버비는 미미 |
| 300만~500만원 (표준 파일럿) | ~5만원 | 서버비는 미미 |
| 월 구독 (정식 운영) | ~5만원 | 월 구독으로 커버 가능 |

**결론**: 서버비 자체는 파일럿 가격에 비해 크지 않습니다. 비용의 주요 부분은 인력(개발, 운영)입니다.

### 추가 비용

| 항목 | 비용 | 설명 |
|------|------|------|
| **도메인** | 연 15,000~30,000원 | .co.kr 또는 .com |
| **SSL** | 0원 | Let's Encrypt 무료 |
| **AI provider** | 사용량에 따라 | DeepSeek 등, 파일럿에서는 미미 |
| **운영 관리** | 인력 비용 | 정기 점검, 백업 확인, 지원 |

---

## 14. 장애 대응 계획

### 장애 유형별 대응

| 장애 유형 | 대응 | 우선순위 |
|----------|------|---------|
| **VM 재부팅** | OCI 콘솔에서 재부팅, Docker 자동 시작 확인 | 높음 |
| **Docker container 재시작** | `docker compose restart` | 높음 |
| **DB 복원 필요** | 백업에서 복원 (`bench restore`) | 높음 |
| **SSL 만료** | certbot 갱신 (`certbot renew`) | 중간 |
| **디스크 가득 참** | 불필요 파일 삭제, 볼륨 확장 | 높음 |
| **AI provider 장애** | MockProvider fallback, degraded mode | 중간 |
| **ERPNext 업데이트 실패** | 백업에서 복원, 업데이트 롤백 | 높음 |
| **네트워크 장애** | OCI 네트워크 확인, 보안 그룹 확인 | 높음 |

### 장애 대응 절차

```
1. 장애 감지 (모니터링 또는 사용자 보고)
2. 영향 범위 확인 (전체 접속 불가 vs 일부 기능 장애)
3. 긴급 대응 (container restart, VM 재부팅)
4. 원인 분석 (로그 확인, 에러 메시지 분석)
5. 복구 (백업 복원, 설정 수정)
6. 사후 처리 (원인 기록, 재발 방지)
```

---

## 15. 하지 않을 것

### 이 문서에서 하지 않는 것

| 하지 않을 것 | 이유 |
|-------------|------|
| **실제 VM 생성** | 계획 문서만 작성 |
| **실제 도메인 설정** | 계획 문서만 작성 |
| **실제 SSL 발급** | 계획 문서만 작성 |
| **실제 credential 기록** | 보안 원칙 |
| **Production compose 확정** | 실제 배포 시 검토 |
| **고객 데이터 사용** | 보안 원칙 |

---

## 16. 후속 실행 PR/Issue 후보

### 구현 순서

| 순위 | PR/Issue 제목 | 설명 |
|------|--------------|------|
| 1 | `docs: define production Docker compose checklist` | Production compose 구성 체크리스트 |
| 2 | `infra: create Oracle Cloud provisioning checklist` | VM 생성 단계별 체크리스트 |
| 3 | `ops: add backup and restore runbook` | 백업/복원 상세 절차 |
| 4 | `ops: add security hardening checklist` | 보안 강화 체크리스트 |
| 5 | `feat: prepare padiem_ai app deployment plan` | Custom App 배포 계획 |
| 6 | `test: cloud deployment smoke test` | 클라우드 배포 후 검증 테스트 |

---

**문서 버전**: v1.0
**작성일**: 2026-05-18
**상태**: Draft
