from app.core.openai_client import client
import json


async def generate_feedback(question: str, answer: str):

    prompt = f"""
    아래는 면접 질문과 지원자의 답변이다.

    [질문]
    {question}

    [답변]
    {answer}

    아래 기준으로 평가 결과를 생성해라.

    요구사항:
    - 질문과 답변의 적합도를 기준으로 0~100점 점수 부여
    - 한 줄 정도의 간단한 피드백 작성
    - 답변에서 반복적으로 사용된 단어 또는 문장이 있는 경우 이를 고려하여 감점 요소로 반영하라
      (예: 같은 단어 과도한 반복, 불필요한 문장 반복, 습관적 표현 반복 등)

    반드시 아래 JSON 형식으로만 응답해라.

    {{
        "score": 85,
        "feedback": "질문 의도에 잘 맞는 답변입니다. 다만 특정 단어 반복이 있어 표현 다양성을 개선하면 좋습니다."
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