import librosa
import numpy as np


async def analyze_voice(
    audio_path: str,
    text: str
):

    y, sr = librosa.load(audio_path)

    # 전체 길이
    total_duration = librosa.get_duration(
        y=y,
        sr=sr
    )

    # 발화 구간 추출
    intervals = librosa.effects.split(
        y,
        top_db=25
    )

    speech_duration = sum(
        (end - start) / sr
        for start, end in intervals
    )

    # 무음 비율
    pause_ratio = (
        (total_duration - speech_duration)
        / total_duration
        if total_duration > 0 else 0
    )

    # Pitch 분석
    f0, _, _ = librosa.pyin(
        y,
        fmin=librosa.note_to_hz("C2"),
        fmax=librosa.note_to_hz("C7")
    )

    pitch_values = f0[~np.isnan(f0)]

    if len(pitch_values) > 0:
        pitch_mean = float(np.mean(pitch_values))
        pitch_std = float(np.std(pitch_values))
    else:
        pitch_mean = 0
        pitch_std = 0

    # Energy 분석 (RMS)
    rms = librosa.feature.rms(y=y)[0]

    energy_mean = float(np.mean(rms))
    energy_std = float(np.std(rms))

    # CPM 계산
    char_count = len(text.replace(" ", ""))

    speech_minutes = (
        speech_duration / 60
        if speech_duration > 0 else 1
    )

    cpm = char_count / speech_minutes

    # 한국어 보정
    # 한국어 CPM 350~450 ≈ 영어 WPM 120~160 체감
    speaking_speed = cpm * 0.35

    # Speaking Speed 상태
    if speaking_speed < 100:
        speed_status = "SLOW"

    elif speaking_speed <= 150:
        speed_status = "IDEAL"

    else:
        speed_status = "FAST"

    # Pitch 상태
    if pitch_std < 15:
        pitch_status = "FLAT"

    elif pitch_std <= 40:
        pitch_status = "STABLE"

    else:
        pitch_status = "EXPRESSIVE"

    # Energy 상태
    if energy_std < 0.02:
        energy_status = "STABLE"

    elif energy_std <= 0.05:
        energy_status = "DYNAMIC"

    else:
        energy_status = "UNSTABLE"

    return {
        "speaking_speed": round(speaking_speed),
        "speed_status": speed_status,

        # 억양 변화량
        "pitch_variation": round(pitch_std),
        "pitch_status": pitch_status,

        # 음성 에너지
        "voice_energy": round(energy_mean, 4),
        "energy_status": energy_status,

    }