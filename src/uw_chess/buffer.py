import pyaudio
from pydub import AudioSegment, silence
from datetime import datetime
from io import BytesIO
from stt import STT

class AudioRecorder:
    def __init__(self, buffer_duration=3000, silence_thresh=-30, silence_duration=2000, export_path='./'):
        self.buffer_duration = buffer_duration
        self.silence_thresh = silence_thresh
        self.silence_duration = silence_duration
        self.export_path = export_path
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.chunk_size = 1024
        self.stt = STT()

    def export_audio(self, buffer, filename):
        """
        Export the audio buffer to a file.
        :param buffer: The AudioSegment buffer to export
        :param filename: The filename for the exported audio
        """
        buffer.export(filename, format='wav')

    def record(self):

        p = pyaudio.PyAudio()
        stream = p.open(format=self.audio_format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk_size)

        buffer = AudioSegment.silent(duration=0)
        accumulated_duration = 0

        while True:
            frames = []
            for _ in range(0, int(self.rate / self.chunk_size * 1)): # Record for 1 second
                try:
                    data = stream.read(self.chunk_size)
                    frames.append(data)
                except IOError as e:
                    if e.errno == pyaudio.paInputOverflowed:
                        continue

            chunk = AudioSegment(data=b''.join(frames), sample_width=p.get_sample_size(self.audio_format), frame_rate=self.rate, channels=self.channels)
            buffer += chunk
            accumulated_duration += len(chunk)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self.export_audio(buffer, f'{self.export_path}recording_{timestamp}.wav')

            # Break condition (if you want to stop recording after a certain duration)
            if accumulated_duration >= self.buffer_duration:
                break
            return buffer.raw_data
