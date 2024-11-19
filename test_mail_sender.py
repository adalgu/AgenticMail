from mail_sender import MailSender
from dotenv import load_dotenv
import os


def test_send_mail():
    # 메일 발송 테스트
    sender = MailSender()

    # 테스트 메일 내용
    to_email = "테스트@gmail.com"
    subject = "AgenticMail Test Message"
    body = """
    안녕하세요,
    
    이 메일은 AgenticMail 프로젝트의 테스트 메일입니다.
    
    주요 기능:
    1. LLM 기반 메일 분석
    2. 우선순위 자동 판단
    3. 자동 답장 생성
    4. SMTP 메일 발송
    
    이 메일이 정상적으로 수신되었다면 메일 발송 기능이 정상적으로 작동하는 것입니다.
    
    감사합니다.
    AgenticMail 테스트 시스템
    """

    # 메일 발송
    result = sender.send_mail(to_email, subject, body)

    if result:
        print("테스트 메일 발송 성공!")
    else:
        print("테스트 메일 발송 실패.")


if __name__ == "__main__":
    test_send_mail()
