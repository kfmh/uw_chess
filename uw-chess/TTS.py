from gtts import gTTS
import io
from pydub import AudioSegment
from pydub.playback import play
from runtime_test import LogExecutionTime

class TTS_move:
    def __init__(self):
        pass

    @LogExecutionTime
    def speech(self, text_str):
        language = 'en'
        promotion  = {"n": "knight", "q": "queen", "b": "bishop", "p": "pawn"}
        if len(text_str) == 5:
            tts_formatting = text_str[:2] + " to " + text_str[2:4] + " promot to " + promotion[text_str[-1]]
        else:
            tts_formatting = text_str[:2] + " to " + text_str[2:]

        # Create a gTTS object
        myobj = gTTS(text=tts_formatting, lang=language, slow=False)

        # Create a BytesIO object and save the gTTS audio data to it
        mp3_fp = io.BytesIO()
        myobj.write_to_fp(mp3_fp)
        mp3_fp.seek(0)  # Move to the beginning of the BytesIO object

        # Load the audio from the BytesIO object
        audio = AudioSegment.from_file(mp3_fp, format="mp3")

        # Play the audio
        play(audio)