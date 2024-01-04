# ============================================================================
# STT.py
# 
# ============================================================================

from runtime_test import LogExecutionTime
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import torch
import numpy as np
from time import sleep
import logging

# Set logging level to ERROR to suppress warnings
logging.getLogger("transformers").setLevel(logging.ERROR)

class STT:
    def __init__(self):

        self.mps_device = torch.device("mps")
        self.torch_dtype = torch.float16
        self.model_id = "distil-whisper/distil-large-v2"

        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            self.model_id, 
            torch_dtype=self.torch_dtype, 
            low_cpu_mem_usage=True, 
            use_safetensors=True
        )

    def analyse(self, audio_segment):

        self.model.to(self.mps_device)

        processor = AutoProcessor.from_pretrained(self.model_id)
        audio_np_array = np.frombuffer(audio_segment, dtype=np.int16)
        

        pipe = pipeline(
            "automatic-speech-recognition",
            model = self.model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            max_new_tokens = 128,
            torch_dtype=self.torch_dtype,
            device = self.mps_device,
        )

        result = pipe(audio_np_array)

        return result["text"]
