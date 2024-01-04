# from print_document import Create_Document
from stt import STT
from multiprocessing import Process, Queue
from time import sleep
import pyaudio
from pydub import AudioSegment, silence
from datetime import datetime

class AudioAnalyzer:
    def __init__(self, queue, game_queue):
        self.queue = queue
        self.game_queue = game_queue
        self.stt = STT()  # Speech-to-text processor
        # self.printing = Create_Document()  # Document creation
        self.stt_text = ""

    def process_analyze(self, name):
        print(f"Start: {name}")
        while True:
            data = self.queue.get()
            if data == "STOP":
                break

            text = self.stt.analyse(data[0])
            # self.printing.document(text, data[1])
            self.stt_text = text
            self.game_queue.put(text)



class AudioRecorder:
    def __init__(self, queue):
        self.queue = queue
        self.silence_thresh = -30
        self.silence_duration = 1000
        self.export_path = './test_audio/'
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 22050
        self.chunk_size = 2048
        self.record_duration = 0.5

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.audio_format, channels=self.channels, 
                                  rate=self.rate, input=True, 
                                  frames_per_buffer=self.chunk_size)

    def process_rec(self, name):
        print(f"Start: {name}")
        buffer = AudioSegment.silent(duration=0)
        accumulated_duration = 0

        while True:
            flushing = False
            frames = []
            for _ in range(0, int(self.rate / self.chunk_size * self.record_duration)):
                try:
                    data = self.stream.read(self.chunk_size)
                    frames.append(data)
                except IOError as e:
                    if e.errno == pyaudio.paInputOverflowed:
                        continue

            chunk = AudioSegment(data=b''.join(frames), 
                                 sample_width=self.p.get_sample_size(self.audio_format), 
                                 frame_rate=self.rate, 
                                 channels=self.channels)
            buffer += chunk
            accumulated_duration += len(chunk)
            data = buffer.raw_data

            if len(buffer) >= self.silence_duration and silence.detect_silence(buffer[-self.silence_duration:], min_silence_len=self.silence_duration, silence_thresh=self.silence_thresh):
                buffer = AudioSegment.silent(duration=0)
                flushing = True

            self.queue.put((data, flushing))
            data = self.queue.get()
            if data == "stop":
                break

