# XConnect License API 사용 가이드

## 📋 목차
- [프로젝트 개요](#프로젝트-개요)
- [시스템 요구사항](#시스템-요구사항)
- [설치 및 설정](#설치-및-설정)
- [서버 실행 방법](#서버-실행-방법)
- [계정별 실행 가이드](#계정별-실행-가이드)
- [API 사용법](#api-사용법)
- [트러블슈팅](#트러블슈팅)

---

## 프로젝트 개요

**XConnect License API**는 Recap Voice 라이선스를 검증하는 FastAPI 기반 REST API 서버입니다.

### 주요 기능
- 라이선스 번호 검증
- 계약 만료일 확인
- 라인 제한 검사
- MySQL 데이터베이스 연동

### 기술 스택
- **Python 3.12+**
- **FastAPI** - 웹 프레임워크
- **Uvicorn** - ASGI 서버
- **MySQL Connector** - 데이터베이스 연결
- **python-dotenv** - 환경변수 관리

---

## 시스템 요구사항

### 필수 요구사항
- Python 3.12 이상
- MySQL 8.0 이상
- Linux 서버 (Ubuntu/CentOS 권장)

### 필수 Python 패키지
```bash
fastapi
uvicorn
mysql-connector-python
python-dotenv
```

---

## 설치 및 설정

### 1. 프로젝트 디렉토리 구조
```
/home/xconnect-license/
├── license_server_fastapi.py  # FastAPI 애플리케이션
├── .env                        # 환경변수 설정 (중요!)
├── .env.example                # 환경변수 템플릿
├── venv/                       # Python 가상환경
└── .claude/                    # 문서 폴더
    └── usage-guide.md          # 이 파일
```

### 2. 환경변수 설정 (.env)

**중요**: `.env` 파일에 데이터베이스 접속 정보를 설정해야 합니다.

`.env.example` 파일을 복사하여 실제 정보로 수정:
```bash
cp .env.example .env
nano .env
```

### 3. 가상환경 설정

```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate

# 패키지 설치
pip install fastapi uvicorn mysql-connector-python python-dotenv
```

---

## 서버 실행 방법

### 개발 모드 (수동 실행)

```bash
# 가상환경 활성화
source /home/xconnect-license/venv/bin/activate

# 서버 실행
uvicorn license_server_fastapi:app --host 127.0.0.1 --port 3022 --reload
```

### 프로덕션 모드 (systemd 서비스)

서버에서는 **systemd**를 통해 자동 시작 및 관리됩니다.

```bash
# 서비스 시작
sudo systemctl start xconnect-license

# 서비스 중지
sudo systemctl stop xconnect-license

# 서비스 재시작
sudo systemctl restart xconnect-license

# 서비스 상태 확인
sudo systemctl status xconnect-license

# 부팅 시 자동 시작 설정
sudo systemctl enable xconnect-license
```

---

## 계정별 실행 가이드

### 🔴 root 계정 실행 (시스템 관리)

root 계정은 **시스템 레벨 작업**만 수행합니다.

#### root 권한이 필요한 작업

#### 1. systemd 서비스 설정 생성/수정
```bash
sudo nano /etc/systemd/system/xconnect-license.service
```

**서비스 설정 내용:**
```ini
[Unit]
Description=XConnect License API (FastAPI)
After=network.target

[Service]
Type=simple
User=xconnect-license
Group=xconnect-license
WorkingDirectory=/home/xconnect-license
EnvironmentFile=/home/xconnect-license/.env
ExecStart=/home/xconnect-license/venv/bin/uvicorn license_server_fastapi:app --host 127.0.0.1 --port 3022
Restart=always
RestartSec=3
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

**중요 포인트:**
- `User=xconnect-license` - 서비스는 xconnect-license 계정으로 실행
- `EnvironmentFile=/home/xconnect-license/.env` - 환경변수 자동 로드
- `WorkingDirectory=/home/xconnect-license` - 작업 디렉토리 지정

#### 2. 서비스 등록 및 관리
```bash
# systemd 설정 리로드
sudo systemctl daemon-reload

# 서비스 시작
sudo systemctl start xconnect-license

# 서비스 상태 확인
sudo systemctl status xconnect-license

# 부팅 시 자동 시작 설정
sudo systemctl enable xconnect-license

# 로그 확인
sudo journalctl -u xconnect-license -f
```

#### 3. 전체 시스템 로그 확인
```bash
# 실시간 로그 모니터링
sudo journalctl -u xconnect-license -f

# 최근 100줄 로그 확인
sudo journalctl -u xconnect-license -n 100

# 특정 시간대 로그 확인
sudo journalctl -u xconnect-license --since "2024-01-01 10:00:00"
```

#### 4. 방화벽 설정 (필요시)
```bash
# 포트 3022 열기
sudo firewall-cmd --permanent --add-port=3022/tcp
sudo firewall-cmd --reload

# 또는 ufw 사용 시
sudo ufw allow 3022/tcp
```

#### 5. 사용자 계정 관리
```bash
# xconnect-license 계정 생성 (최초 1회)
sudo useradd -r -s /bin/bash -d /home/xconnect-license -m xconnect-license

# 계정 권한 확인
sudo -u xconnect-license whoami
```

---

### 🟢 xconnect-license 계정 실행 (애플리케이션 관리)

xconnect-license 계정은 **애플리케이션 코드 및 설정**을 관리합니다.

#### xconnect-license 계정으로 전환
```bash
sudo su - xconnect-license
```

#### xconnect-license 계정으로 수행하는 작업

#### 1. 코드 수정
```bash
# 작업 디렉토리로 이동
cd /home/xconnect-license

# 코드 수정
nano license_server_fastapi.py
```

#### 2. 환경변수 설정 수정
```bash
# .env 파일 수정
nano .env

# 주의: 수정 후 반드시 서비스 재시작 필요
exit  # xconnect-license 계정 종료
sudo systemctl restart xconnect-license
```

#### 3. 패키지 설치 및 업데이트
```bash
# 가상환경 활성화
source venv/bin/activate

# 패키지 설치
pip install <패키지명>

# 패키지 업데이트
pip install --upgrade <패키지명>

# 설치된 패키지 확인
pip list

# 가상환경 종료
deactivate
```

#### 4. 수동 테스트 실행
```bash
# 가상환경 활성화
source venv/bin/activate

# 개발 서버 실행 (다른 포트 사용)
uvicorn license_server_fastapi:app --host 127.0.0.1 --port 8000 --reload

# 종료: Ctrl + C
```

#### 5. 로그 확인 (사용자 레벨)
```bash
# 서비스 상태만 확인 (sudo 없이)
systemctl status xconnect-license

# 애플리케이션 에러 확인
tail -f /var/log/syslog | grep xconnect
```

#### 6. 데이터베이스 연결 테스트
```bash
# Python으로 DB 연결 테스트
source venv/bin/activate
python3 -c "
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
    port=int(os.getenv('DB_PORT', 3306))
)
print('✅ Database connection successful!')
conn.close()
"
```

---

## 작업 흐름 요약

### 코드 변경 시 작업 순서

1. **xconnect-license 계정으로 전환**
   ```bash
   sudo su - xconnect-license
   ```

2. **코드 수정**
   ```bash
   cd /home/xconnect-license
   nano license_server_fastapi.py
   ```

3. **xconnect-license 계정 종료**
   ```bash
   exit
   ```

4. **root 권한으로 서비스 재시작**
   ```bash
   sudo systemctl restart xconnect-license
   ```

5. **상태 확인**
   ```bash
   sudo systemctl status xconnect-license
   ```

### 환경변수 변경 시 작업 순서

1. **xconnect-license 계정으로 전환**
   ```bash
   sudo su - xconnect-license
   ```

2. **.env 파일 수정**
   ```bash
   nano .env
   ```

3. **xconnect-license 계정 종료**
   ```bash
   exit
   ```

4. **systemd 서비스 재시작**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl restart xconnect-license
   ```

---

## API 사용법

### 엔드포인트 목록

#### 1. 헬스체크
```bash
GET http://127.0.0.1:3022/
```

**응답 예시:**
```json
{
  "status": "ok",
  "service": "RecapVoice License API"
}
```

#### 2. 라이선스 검증
```bash
POST http://127.0.0.1:3022/check_license
Content-Type: application/json

{
  "license_no": "ABC123",
  "line_count": 5
}
```

**성공 응답 (200 OK):**
```json
{
  "result": true,
  "message": "License valid",
  "contract_end_date": "2025-12-31",
  "line_limit": 10
}
```

**실패 응답 예시:**

- **라이선스 없음:**
  ```json
  {
    "result": false,
    "message": "License not found"
  }
  ```

- **만료됨:**
  ```json
  {
    "result": false,
    "message": "License expired"
  }
  ```

- **라인 제한 초과:**
  ```json
  {
    "result": false,
    "message": "Exceeded max lines"
  }
  ```

### cURL 예시

```bash
# 헬스체크
curl http://127.0.0.1:3022/

# 라이선스 검증
curl -X POST http://127.0.0.1:3022/check_license \
  -H "Content-Type: application/json" \
  -d '{
    "license_no": "ABC123",
    "line_count": 5
  }'
```

---

## 트러블슈팅

### 1. 서비스가 시작되지 않음

**증상:**
```bash
sudo systemctl status xconnect-license
# Active: failed (Result: exit-code)
```

**해결 방법:**

```bash
# 상세 로그 확인
sudo journalctl -u xconnect-license -n 50

# 일반적인 원인:
# 1. .env 파일 없음
sudo -u xconnect-license ls -la /home/xconnect-license/.env

# 2. 가상환경 경로 오류
sudo -u xconnect-license ls -la /home/xconnect-license/venv/bin/uvicorn

# 3. 포트 이미 사용 중
sudo netstat -tulpn | grep 3022
```

### 2. MySQL 연결 실패

**증상:**
```
Can't connect to MySQL server on '1.234.2.37:3306'
```

**해결 방법:**

```bash
# 1. 환경변수 확인
sudo -u xconnect-license bash -c "source /home/xconnect-license/.env && env | grep DB_"

# 2. systemd 서비스에서 환경변수 로드 확인
sudo systemctl cat xconnect-license | grep EnvironmentFile

# 3. MySQL 서버 연결 테스트
mysql -h 1.234.2.37 -P 3306 -u xconnect_admin -p

# 4. 방화벽 확인
sudo firewall-cmd --list-all
```

### 3. 날짜 비교 오류

**증상:**
```
can't compare datetime.datetime to datetime.date
```

**해결 방법:**
코드에 이미 수정되어 있습니다. (datetime → date 변환 로직 추가)

### 4. 환경변수 로드 안 됨

**증상:**
```
DB_HOST is None
```

**해결 방법:**

```bash
# systemd 서비스 파일 수정
sudo nano /etc/systemd/system/xconnect-license.service

# 다음 줄 추가 (없는 경우):
EnvironmentFile=/home/xconnect-license/.env

# 재시작
sudo systemctl daemon-reload
sudo systemctl restart xconnect-license
```

### 5. 권한 문제

**증상:**
```
Permission denied: '/home/xconnect-license/.env'
```

**해결 방법:**

```bash
# 파일 소유권 변경
sudo chown xconnect-license:xconnect-license /home/xconnect-license/.env
sudo chmod 600 /home/xconnect-license/.env

# 전체 디렉토리 권한 확인
sudo chown -R xconnect-license:xconnect-license /home/xconnect-license
```

### 6. 포트 충돌

**증상:**
```
Address already in use
```

**해결 방법:**

```bash
# 포트 사용 중인 프로세스 확인
sudo netstat -tulpn | grep 3022

# 프로세스 종료
sudo kill -9 <PID>

# 또는 다른 포트 사용
# systemd 서비스 파일에서 --port 3022를 다른 포트로 변경
```

---

## 보안 권장사항

### 1. .env 파일 보안
```bash
# .env 파일은 소유자만 읽기 가능
chmod 600 /home/xconnect-license/.env

# Git에 절대 커밋하지 말 것 (이미 .gitignore에 포함됨)
```

### 2. 데이터베이스 비밀번호
- 정기적으로 비밀번호 변경
- 복잡한 비밀번호 사용
- 외부 노출 금지

### 3. API 서버 보안
- 현재는 `127.0.0.1`로만 접근 가능 (외부 차단)
- 외부 노출 시 HTTPS 사용 필수
- API 키 인증 추가 권장

### 4. 방화벽 설정
```bash
# 필요한 포트만 열기
sudo firewall-cmd --permanent --add-port=3022/tcp
sudo firewall-cmd --reload
```

---

## 유지보수 체크리스트

### 일일 점검
- [ ] 서비스 상태 확인: `sudo systemctl status xconnect-license`
- [ ] 로그 확인: `sudo journalctl -u xconnect-license -n 100`
- [ ] API 응답 테스트: `curl http://127.0.0.1:3022/`

### 주간 점검
- [ ] 데이터베이스 연결 테스트
- [ ] 디스크 용량 확인: `df -h`
- [ ] 메모리 사용량 확인: `free -h`

### 월간 점검
- [ ] Python 패키지 업데이트
- [ ] 보안 패치 적용
- [ ] 백업 확인

---

## 참고 자료

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Uvicorn 문서](https://www.uvicorn.org/)
- [systemd 서비스 가이드](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
- [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/)

---

## 문의 및 지원

문제 발생 시 다음 정보를 포함하여 문의:

1. 서비스 상태: `sudo systemctl status xconnect-license`
2. 최근 로그: `sudo journalctl -u xconnect-license -n 100`
3. 환경 정보: Python 버전, OS 버전
4. 에러 메시지 전문

---

**작성일:** 2025-01-XX
**버전:** 1.0
**작성자:** Claude Code
