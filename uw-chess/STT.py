import speech_recognition as sr 
from time import sleep
from UCI_formatting import formatting
from runtime_test import LogExecutionTime


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
        recoding = True
        
        while recoding:
            with CustomMicrophone() as source:
                print("Listening....")
                audio = self.Recognize.listen(source, 
                                            timeout=None, 
                                            phrase_time_limit=phrase_timeout)
                print("Stop Listening....")
                try:
                    text = self.Recognize.recognize_google(audio)
                    print(text)
                    uci = self.formatting.uci_str(text)
                    if len(uci) < 6:
                        recoding = False
                        return uci
                except sr.UnknownValueError:
                    # If the audio wasn't understood, it's ok to just keep listening
                    pass
                except sr.RequestError:
                    print("API unavailable. Please check your internet connection")
                    sleep(2)
