from app.core.openai_client import client
import json


async def generate_feedback(
        question: str,
        answer: str,
        field_name: str = None,
        company_name: str = None
):
    field_context = ""
    company_context = ""

    if field_name:
        field_context = f"""
    [지원 분야]
    {field_name}

    * 추가 지시사항:
    지원 분야({field_name})에서 현재 실무적으로 가장 요구되는 핵심 역량이나 트렌드를 파악하고,
    지원자의 답변이 해당 역량을 얼마나 잘 어필하고 있는지 피드백 내용에 반드시 반영할 것.
    """

    if company_name:
        company_context = f"""
    [희망 기업]
    {company_name}

    * 추가 지시사항:
    {company_name}이 최근 추구하는 인재상, 핵심 가치, 조직 문화,
    채용 방향성 등을 분석하여 지원자의 답변이 해당 기업과 얼마나 적합한지 평가에 반영할 것.

    단, 과도한 추측은 피하고 일반적으로 알려진 기업 성향 및 채용 방향을 기반으로 판단할 것.
    """

    prompt = f"""
    아래는 면접 질문과 지원자의 답변이다.

    {field_context}

    {company_context}

    [질문]
    {question}

    [답변]
    {answer}

    너는 면접 평가자다.

    아래 평가 기준에 따라 답변을 분석하여 점수를 계산하고 점수와 함께 한줄 피드백을 제공하라.

    [평가 기준]

    1. 질문 적합성 (0~40)
    - 질문 의도를 정확히 이해했는가
    - 질문에 맞는 핵심 경험 또는 근거가 포함되었는가
    - 질문과 관련 없는 내용이 과도하지 않은가

    2. 답변 구조 (0~20)
    - 답변 흐름이 자연스러운가
    - 도입, 설명, 결과가 논리적으로 연결되는가
    - 문장이 지나치게 산만하지 않은가

    3. 전달력 및 명확성 (0~20)
    - 문장이 이해하기 쉬운가
    - 핵심 메시지가 명확하게 전달되는가
    - 표현이 지나치게 모호하지 않은가

    4. 반복 표현 여부 (0~20)
    - 같은 단어 또는 문장을 과도하게 반복하지 않았는가
    - "음", "약간", "그냥" 등의 습관적 표현이 많은가
    - 표현 다양성이 유지되는가

    [점수 기준]

    - 90~100점:
    질문 의도를 정확히 파악했고 답변 구조와 전달력이 매우 우수함

    - 80~89점:
    전반적으로 우수하나 일부 표현 또는 구체성이 부족함

    - 70~79점:
    기본적인 답변은 가능하지만 핵심 근거 또는 논리성이 부족함

    - 60~69점:
    반복 표현이 많거나 답변 핵심 내용이 일부 누락됨

    - 0~59점:
    질문과 관련성이 낮거나 전달력이 크게 부족함

    반드시 아래 JSON 형식으로만 응답해라.

    {{
        "score": 85,
        "feedback": "질문 의도에 적절하게 답변했지만 일부 표현 반복이 존재합니다."
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "너는 냉정한 면접 평가자다. "
                    "항상 JSON 객체 형식으로만 응답한다."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"}
    )

    result_text = response.choices[0].message.content

    try:
        result = json.loads(result_text)

    except json.JSONDecodeError:
        result = {
            "score": 0,
            "feedback": "피드백 생성 실패"
        }

    return result