from app.core.openai_client import client

async def analyze_text(text: str):
    prompt = f"""
    다음은 면접 지원자의 답변이다:
    "{text}"

    아래 기준으로 평가하고 JSON으로 반환해:

    1. relevance: 질문 의도에 적절한가 (0~10)
    2. structure: 답변 구조가 명확한가 (0~10)
    3. clarity: 전달력이 좋은가 (0~10)
    4. conciseness: 불필요하게 길지 않은가 (0~10)
    5. strengths: 잘한 점
    6. weaknesses: 부족한 점
    7. improved_answer: 더 나은 모범 답변
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "너는 냉정한 면접관이다."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content