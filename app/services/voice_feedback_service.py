async def generate_voice_feedback(
    analysis_result: dict
):

    feedbacks = []

    pitch_std = analysis_result["pitch_std"]
    pause_ratio = analysis_result["pause_ratio"]
    volume_std = analysis_result["volume_std"]

    # 억양 분석
    if pitch_std < 20:
        feedbacks.append(
            "억양 변화가 적어 다소 단조롭게 들릴 수 있습니다."
        )

    elif pitch_std < 40:
        feedbacks.append(
            "억양 변화가 자연스러운 편입니다."
        )

    else:
        feedbacks.append(
            "억양 변화가 풍부하여 전달력이 좋습니다."
        )

    # 침묵 분석
    if pause_ratio > 0.4:
        feedbacks.append(
            "침묵 구간이 긴 편입니다."
        )

    elif pause_ratio > 0.25:
        feedbacks.append(
            "적절한 pause가 포함되어 있습니다."
        )

    else:
        feedbacks.append(
            "답변 흐름이 자연스럽습니다."
        )

    # 음량 안정성
    if volume_std > 0.05:
        feedbacks.append(
            "목소리 크기 변화가 커 다소 불안정하게 들릴 수 있습니다."
        )

    else:
        feedbacks.append(
            "안정적인 목소리 톤을 유지하고 있습니다."
        )

    return {
        "voice_feedback": feedbacks
    }