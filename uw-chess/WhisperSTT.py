import speech_recognition as sr 
import io, json, requests

import os

key = os.getenv("HFwrite")

class CustomMicrophone(sr.Microphone):
    def __init__(self, *args, **kwargs):
        kwargs['sample_rate'] = 16000
        super(CustomMicrophone, self).__init__(*args, **kwargs)

class RecordVoice:
    def __init__(self):
        self.headers = {"Authorization": f"Bearer {key}"}
        self.API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v2"
        self.Recognize = sr.Recognizer()
        self.Mic = CustomMicrophone()  # Use CustomMicrophone instead
        with CustomMicrophone() as source:  # Use CustomMicrophone instead
            self.Recognize.adjust_for_ambient_noise(source)

    def listen_for_keyword(self, 
                           keyword="activate", 
                           phrase_timeout=None):

        with CustomMicrophone() as source:
            print("Listening....")
            audio = self.Recognize.listen(source, 
                                          timeout=None, 
                                          phrase_time_limit=phrase_timeout)
            try:
                text = self.Recognize.recognize_google(audio)
                if keyword in text:
                    print("== Activate ==")
                    return True
            except sr.UnknownValueError:
                # If the audio wasn't understood, it's ok to just keep listening
                print("activate_function?")
                pass
            except sr.RequestError:
                print("API unavailable. Please check your internet connection")
                return False

    def speech_to_text(self,
                       phrase_timeout=None):
        self.Recognize.pause_threshold = 0.8
        with CustomMicrophone() as source:
            print("start Rec STT")
            audio = self.Recognize.listen(source, 
                                          timeout=None, 
                                          phrase_time_limit=phrase_timeout)
        
            # Convert to WAV bytes
            audio_bytes = audio.get_wav_data()
            # Convert to BytesIO object
            audio_io = io.BytesIO(audio_bytes)

            print("end Rec STT")
            try:

                response = requests.request("POST", self.API_URL, headers=self.headers, data=audio_io)
                transcription = json.loads(response.content.decode("utf-8"))

                return transcription
                
            except sr.UnknownValueError:
                # If the audio wasn't understood, it's okay to just keep listening
                print("stt")
                pass
            except sr.RequestError:
                print("API unavailable. Please check your internet connection")
                return False
