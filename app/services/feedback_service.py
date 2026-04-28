from app.core.openai_client import client
import json

async def generate_feedback(question: str, answer: str):
    prompt = f"""
    아래는 면접 질문과 지원자의 답변이다.

    [질문]
    {question}

    [답변]
    {answer}

    아래 형식으로 평가 결과를 생성해라.

    요구사항:
    - 질문과 답변의 적합도를 기준으로 0~100점 점수 부여
    - 한 줄 정도의 간단한 피드백 작성

    출력 형식(JSON):
    {{
        "score": 85,
        "feedback": "질문 의도에 잘 맞는 답변입니다. 다만 구체적인 사례를 추가하면 더 좋습니다."
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "너는 면접 평가자다."},
            {"role": "user", "content": prompt}
        ]
    )

    result_text = response.choices[0].message.content

    # JSON 파싱
    try:
        result = json.loads(result_text)
    except:
        # fallback (모델이 형식 어길 때 대비)
        result = {
            "score": 0,
            "feedback": result_text
        }

    return result