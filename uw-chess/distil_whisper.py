import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import speech_recognition as sr 
import numpy as np

class CustomMicrophone(sr.Microphone):
    def __init__(self, *args, **kwargs):
        kwargs['sample_rate'] = 16000
        super(CustomMicrophone, self).__init__(*args, **kwargs)

class RecordVoice:
    def __init__(self):
        self.Recognize = sr.Recognizer()
        self.Mic = CustomMicrophone()  # Use CustomMicrophone instead
        with CustomMicrophone() as source:  # Use CustomMicrophone instead
            self.Recognize.adjust_for_ambient_noise(source)

        self.mps_device = torch.device("mps")
        self.torch_dtype = torch.float16
        self.model_id = "distil-whisper/distil-large-v2"

        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            self.model_id, torch_dtype=self.torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        )

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

                print("end Rec STT")
                try:
                    self.model.to(self.mps_device)

                    processor = AutoProcessor.from_pretrained(self.model_id)

                    # Convert AudioData to numpy ndarray
                    audio_np_array = np.frombuffer(audio.frame_data, dtype=np.int16)

                    pipe = pipeline(
                        "automatic-speech-recognition",
                        model=self.model,
                        tokenizer=processor.tokenizer,
                        feature_extractor=processor.feature_extractor,
                        max_new_tokens=128,
                        torch_dtype=self.torch_dtype,
                        device=self.mps_device,
                    )
                    return pipe(audio_np_array)
                    
                except sr.UnknownValueError:
                    # If the audio wasn't understood, it's okay to just keep listening
                    print("stt")
                    pass
                except sr.RequestError:
                    print("API unavailable. Please check your internet connection")
                    return False