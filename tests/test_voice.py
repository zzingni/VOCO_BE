import asyncio

from app.services.voice_analysis_service import (
    analyze_voice
)


async def main():

    audio_path = "tests/test.wav"

    text = """
    안녕하세요 이번 채용에 지원하게 된 권지은이라고 합니다.
    """

    analysis_result = await analyze_voice(
        audio_path,
        text
    )

    print("\n[음성 분석 결과]")
    print(analysis_result)


asyncio.run(main())