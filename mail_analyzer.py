import openai
from dotenv import load_dotenv
import os
from typing import Dict, Any

# .env 파일 로드
load_dotenv()


class MailAnalyzer:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key

    def analyze_mail(self, subject: str, body: str, sender: str) -> Dict[str, Any]:
        """
        이메일 내용을 분석하여 우선순위, 긴급도, 필요한 조치 등을 판단

        Args:
            subject (str): 이메일 제목
            body (str): 이메일 본문
            sender (str): 발신자

        Returns:
            Dict[str, Any]: 분석 결과를 담은 딕셔너리
        """
        prompt = f"""
        다음 이메일을 분석해주세요:

        발신자: {sender}
        제목: {subject}
        본문: {body}

        다음 항목들을 평가해주세요:
        1. 우선순위 (1-5, 5가 가장 높음)
        2. 긴급도 (상/중/하)
        3. 답장 필요 여부 (예/아니오)
        4. 필요한 조치사항
        5. 이메일의 주요 의도나 목적
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "당신은 이메일을 분석하고 중요도와 필요한 조치를 판단하는 전문가입니다."},
                    {"role": "user", "content": prompt}
                ]
            )

            # GPT 응답을 구조화된 형태로 파싱
            analysis = self._parse_gpt_response(
                response.choices[0].message.content)
            return analysis

        except Exception as e:
            print(f"메일 분석 중 오류 발생: {e}")
            return {
                "priority": 3,
                "urgency": "중",
                "needs_reply": False,
                "required_actions": ["분석 중 오류 발생"],
                "main_purpose": "분석 실패"
            }

    def generate_reply(self, original_subject: str, original_body: str,
                       sender: str, analysis: Dict[str, Any]) -> str:
        """
        분석 결과를 바탕으로 적절한 답장 생성

        Args:
            original_subject (str): 원본 이메일 제목
            original_body (str): 원본 이메일 본문
            sender (str): 발신자
            analysis (Dict[str, Any]): analyze_mail()의 분석 결과

        Returns:
            str: 생성된 답장 내용
        """
        prompt = f"""
        다음 이메일에 대한 답장을 작성해주세요:

        원본 이메일:
        발신자: {sender}
        제목: {original_subject}
        본문: {original_body}

        분석 결과:
        우선순위: {analysis['priority']}
        긴급도: {analysis['urgency']}
        주요 목적: {analysis['main_purpose']}

        다음 사항을 고려하여 답장을 작성해주세요:
        1. 전문적이고 공손한 톤 유지
        2. 원본 이메일의 모든 중요 포인트에 대한 응답 포함
        3. 필요한 경우 추가 정보 요청
        4. 명확한 다음 단계나 조치사항 제시
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "당신은 전문적인 이메일 답장을 작성하는 전문가입니다."},
                    {"role": "user", "content": prompt}
                ]
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"답장 생성 중 오류 발생: {e}")
            return "답장 생성 중 오류가 발생했습니다."

    def _parse_gpt_response(self, response: str) -> Dict[str, Any]:
        """
        GPT 응답을 구조화된 형태로 파싱

        Args:
            response (str): GPT API 응답 텍스트

        Returns:
            Dict[str, Any]: 파싱된 분석 결과
        """
        # 기본값 설정
        analysis = {
            "priority": 3,
            "urgency": "중",
            "needs_reply": False,
            "required_actions": [],
            "main_purpose": ""
        }

        try:
            # 응답에서 각 항목 추출
            lines = response.split('\n')
            for line in lines:
                line = line.strip().lower()
                if '우선순위' in line or 'priority' in line:
                    priority = [int(s) for s in line if s.isdigit()]
                    if priority:
                        analysis['priority'] = priority[0]
                elif '긴급도' in line or 'urgency' in line:
                    if '상' in line:
                        analysis['urgency'] = '상'
                    elif '하' in line:
                        analysis['urgency'] = '하'
                elif '답장 필요' in line or 'needs reply' in line:
                    analysis['needs_reply'] = '예' in line or 'yes' in line
                elif '조치사항' in line or 'actions' in line:
                    actions = line.split(':')[-1].strip()
                    analysis['required_actions'] = [a.strip()
                                                    for a in actions.split(',')]
                elif '목적' in line or 'purpose' in line:
                    purpose = line.split(':')[-1].strip()
                    analysis['main_purpose'] = purpose

        except Exception as e:
            print(f"GPT 응답 파싱 중 오류 발생: {e}")

        return analysis
