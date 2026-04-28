from app.core.openai_client import client

async def generate_feedback(analysis_json: str):
    prompt = f"""
    다음 면접 평가 결과를 바탕으로 지원자에게 피드백을 제공해:
    {analysis_json}

    요구사항:
    - 실제 면접 코치처럼 말하기
    - 구체적인 개선 방법 제시
    - 실전에서 바로 쓸 수 있는 팁 포함
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "너는 면접 코치다."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content