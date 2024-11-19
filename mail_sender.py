import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
from typing import Optional, List

# .env 파일 로드
load_dotenv()


class MailSender:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.email_account = os.getenv('EMAIL_ACCOUNT')
        self.email_password = os.getenv('EMAIL_PASSWORD')

    def send_mail(self,
                  to_email: str,
                  subject: str,
                  body: str,
                  cc: Optional[List[str]] = None,
                  bcc: Optional[List[str]] = None) -> bool:
        """
        이메일을 발송하는 메서드

        Args:
            to_email (str): 수신자 이메일
            subject (str): 이메일 제목
            body (str): 이메일 본문
            cc (Optional[List[str]]): 참조 수신자 목록
            bcc (Optional[List[str]]): 숨은 참조 수신자 목록

        Returns:
            bool: 발송 성공 여부
        """
        try:
            # 메시지 생성
            msg = MIMEMultipart()
            msg['From'] = self.email_account
            msg['To'] = to_email
            msg['Subject'] = subject

            # CC 추가
            if cc:
                msg['Cc'] = ', '.join(cc)

            # 본문 추가
            msg.attach(MIMEText(body, 'plain'))

            # 모든 수신자 목록 생성
            recipients = [to_email]
            if cc:
                recipients.extend(cc)
            if bcc:
                recipients.extend(bcc)

            # SMTP 서버 연결 및 로그인
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # TLS 보안 연결
                server.login(self.email_account, self.email_password)

                # 메일 발송
                server.sendmail(self.email_account,
                                recipients, msg.as_string())

            print(f"메일 발송 성공: {subject}")
            return True

        except Exception as e:
            print(f"메일 발송 중 오류 발생: {e}")
            return False

    def send_reply(self,
                   to_email: str,
                   original_subject: str,
                   reply_body: str,
                   cc: Optional[List[str]] = None,
                   bcc: Optional[List[str]] = None) -> bool:
        """
        답장 메일을 발송하는 메서드

        Args:
            to_email (str): 수신자 이메일
            original_subject (str): 원본 이메일 제목
            reply_body (str): 답장 본문
            cc (Optional[List[str]]): 참조 수신자 목록
            bcc (Optional[List[str]]): 숨은 참조 수신자 목록

        Returns:
            bool: 발송 성공 여부
        """
        # 답장 제목 생성 (Re: 가 없는 경우에만 추가)
        subject = f"Re: {original_subject}" if not original_subject.startswith(
            'Re:') else original_subject

        return self.send_mail(to_email, subject, reply_body, cc, bcc)
