import speech_recognition as sr 
from time import sleep
from UCI_formatting import formatting
from runtime_test import LogExecutionTime
import asyncio


class CustomMicrophone(sr.Microphone):
    def __init__(self, *args, **kwargs):
        kwargs['sample_rate'] = 16000
        super(CustomMicrophone, self).__init__(*args, **kwargs)

class RecordVoice:
    def __init__(self):
        self.Recognize = sr.Recognizer()
        self.Recognize.pause_threshold = 1.0
        self.Mic = CustomMicrophone()  
        with CustomMicrophone() as source:  
            self.Recognize.adjust_for_ambient_noise(source)
        self.formatting = formatting()

    @LogExecutionTime
    def listen(self, phrase_timeout=None):
        try:
            with CustomMicrophone() as source:
                print("Listening....")
                audio = self.Recognize.listen(source, 
                                            timeout=None, 
                                            phrase_time_limit=None)
                print("Stop Listening....")
                return audio
        
        except sr.RequestError:
            print("API unavailable. Please check your internet connection")
            sleep(1)
            return None
        

    @LogExecutionTime
    async def analyze(self, audio):
        try:
            text = self.Recognize.recognize_google(audio)
            print(text)
            uci = self.formatting.uci_str(text)
            if uci:
                # print(f'uci: {uci} len {len(uci)}')
                return False, uci
            else: 
                return True, "try again" 

        except sr.UnknownValueError:
            # Handle the case where speech is not recognized
            print("Speech was not understood.")
            return True, None
        
        except sr.RequestError as e:
            # Handle API request errors
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return True, None

    
