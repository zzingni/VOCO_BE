# app/utils/audio_converter.py
from pydub import AudioSegment
import os

def convert_to_mp3(input_path):
    output_path = input_path.replace(".wav", ".mp3")

    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format="mp3")

    return output_path