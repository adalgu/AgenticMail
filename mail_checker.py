import poplib
import email
from email.header import decode_header
from dotenv import load_dotenv
import os
from mail_analyzer import MailAnalyzer
from mail_sender import MailSender

# .env 파일 로드
load_dotenv()


class MailChecker:
    def __init__(self):
        # 환경변수에서 연결 정보 가져오기
        self.pop_server = os.getenv('POP3_SERVER')
        self.email_account = os.getenv('EMAIL_ACCOUNT')
        self.password = os.getenv('EMAIL_PASSWORD')

        # 메일 분석기와 발송기 초기화
        self.analyzer = MailAnalyzer()
        self.sender = MailSender()

    def check_mails(self):
        try:
            # POP3 서버 연결
            print(f"서버 연결 시도: {self.pop_server}")
            mail = poplib.POP3_SSL(self.pop_server)
            print("서버 연결 성공")

            print("로그인 시도...")
            mail.user(self.email_account)
            mail.pass_(self.password)
            print("로그인 성공")

            # 메일 정보 가져오기
            num_messages = len(mail.list()[1])
            print(f"총 {num_messages}개의 메일이 있습니다.")

            # 각 메일 확인 및 분석
            for i in range(num_messages):
                self.process_mail(mail, i+1)

            # 연결 종료
            mail.quit()
            print("\n메일 확인이 완료되었습니다.")

        except Exception as e:
            print(f"오류 발생: {e}")
            print("\n다음을 확인해주세요:")
            print("1. POP3 서버 주소가 올바른지")
            print("2. 이메일 계정과 비밀번호가 올바른지")
            print("3. 해당 이메일 서비스에서 POP3 접근이 활성화되어 있는지")
            print("4. 보안 설정에서 '보안 수준이 낮은 앱의 액세스'가 허용되어 있는지")

    def process_mail(self, mail, mail_number):
        """단일 메일을 처리하는 메서드"""
        try:
            # 메일 가져오기
            lines = mail.retr(mail_number)[1]
            message_content = b'\n'.join(lines).decode('utf-8')
            msg = email.message_from_string(message_content)

            # 헤더 정보 읽기
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")
            from_ = msg.get("From")
            print(f"\n처리 중인 메일 #{mail_number}")
            print(f"Subject: {subject}")
            print(f"From: {from_}")

            # 메일 본문 추출
            body = self.get_mail_body(msg)

            # LLM을 통한 메일 분석
            print("\n메일 분석 중...")
            analysis = self.analyzer.analyze_mail(subject, body, from_)

            print("\n분석 결과:")
            print(f"우선순위: {analysis['priority']}")
            print(f"긴급도: {analysis['urgency']}")
            print(f"답장 필요: {'예' if analysis['needs_reply'] else '아니오'}")
            print(f"필요한 조치: {', '.join(analysis['required_actions'])}")
            print(f"주요 목적: {analysis['main_purpose']}")

            # 답장이 필요한 경우 자동 답장 생성 및 발송
            if analysis['needs_reply']:
                print("\n답장 생성 중...")
                reply_body = self.analyzer.generate_reply(
                    subject, body, from_, analysis)

                # 발신자 이메일 주소 추출
                sender_email = email.utils.parseaddr(from_)[1]

                print("답장 발송 중...")
                if self.sender.send_reply(sender_email, subject, reply_body):
                    print("답장이 성공적으로 발송되었습니다.")
                else:
                    print("답장 발송에 실패했습니다.")

        except Exception as e:
            print(f"메일 #{mail_number} 처리 중 오류 발생: {e}")

    def get_mail_body(self, msg):
        """이메일 본문을 추출하는 메서드"""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    return part.get_payload(decode=True).decode()
        else:
            return msg.get_payload(decode=True).decode()
        return ""


if __name__ == "__main__":
    checker = MailChecker()
    checker.check_mails()
