import json
import requests
import io
from pydub import AudioSegment
from pydub.playback import play
import os

key = os.getenv("HFwrite")

class TTS:
    def __init__(self):
        self.headers = {"Authorization": f"Bearer {key}"}
        self.API_URL = "https://api-inference.huggingface.co/models/facebook/fastspeech2-en-ljspeech"

    def speech(self, payload):
        response = requests.post(self.API_URL, headers=self.headers, json=payload)
        audio_bytes = response.content

        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="flac")
        audio = audio.set_sample_width(2)
        play(audio)