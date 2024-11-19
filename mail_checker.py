import poplib
import email
from email.header import decode_header
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# 환경변수에서 연결 정보 가져오기
pop_server = os.getenv('POP3_SERVER')
email_account = os.getenv('EMAIL_ACCOUNT')
password = os.getenv('EMAIL_PASSWORD')

try:
    # POP3 서버 연결
    print(f"서버 연결 시도: {pop_server}")
    mail = poplib.POP3_SSL(pop_server)
    print("서버 연결 성공")

    print("로그인 시도...")
    mail.user(email_account)
    mail.pass_(password)
    print("로그인 성공")

    # 2. 메일 정보 가져오기
    num_messages = len(mail.list()[1])
    print(f"총 {num_messages}개의 메일이 있습니다.")

    # 3. 각 메일 확인 및 분석
    for i in range(num_messages):
        # 메일 가져오기
        lines = mail.retr(i+1)[1]
        message_content = b'\n'.join(lines).decode('utf-8')
        msg = email.message_from_string(message_content)

        # 헤더 정보 읽기
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")
        from_ = msg.get("From")
        print(f"\nSubject: {subject}")
        print(f"From: {from_}")

        # 메일 본문 읽기
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    body = part.get_payload(decode=True).decode()
                    print(f"Body: {body}")
                    # 4. 응답 필요 여부 판단
                    if "please respond" in body.lower() or "asap" in body.lower():
                        print("⚠️ 응답 필요 메일입니다!")
        else:
            body = msg.get_payload(decode=True).decode()
            print(f"Body: {body}")

    # 5. 연결 종료
    mail.quit()
    print("\n메일 확인이 완료되었습니다.")

except Exception as e:
    print(f"오류 발생: {e}")
    print("\n다음을 확인해주세요:")
    print("1. POP3 서버 주소가 올바른지")
    print("2. 이메일 계정과 비밀번호가 올바른지")
    print("3. 해당 이메일 서비스에서 POP3 접근이 활성화되어 있는지")
    print("4. 보안 설정에서 '보안 수준이 낮은 앱의 액세스'가 허용되어 있는지")
