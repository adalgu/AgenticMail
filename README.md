# AgenticMail

이메일을 자동으로 관리하고 처리하는 AI 기반 이메일 에이전트입니다.

## 현재 기능

- POP3를 통한 이메일 수신 및 읽기
- 기본적인 응답 필요 메일 식별 ("please respond", "asap" 키워드 기반)

## 개발 예정 기능

1. **LLM 기반 메일 분석**

   - 메일 내용의 맥락 이해
   - 우선순위 자동 판단
   - 긴급도 평가
   - 카테고리 분류

2. **자동 응답 시스템**

   - LLM을 활용한 맥락에 맞는 답장 초안 작성
   - 메일의 성격과 긴급도에 따른 응답 우선순위 결정
   - SMTP를 통한 자동 답장 발송

3. **이메일 관리 자동화**
   - 중요도에 따른 자동 분류
   - 후속 조치 필요 항목 추적
   - 처리 현황 대시보드

## 설치 및 설정

1. 필요 패키지 설치

```bash
pip install python-dotenv
```

2. 환경 변수 설정
   `.env` 파일을 생성하고 다음 정보를 설정:

```
POP3_SERVER=your_pop3_server
EMAIL_ACCOUNT=your_email
EMAIL_PASSWORD=your_password
```

## 사용 방법

```bash
python mail_checker.py
```

## 기여

프로젝트 개선을 위한 제안이나 풀 리퀘스트를 환영합니다.
