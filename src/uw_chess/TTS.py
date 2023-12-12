# ============================================================================
# TTS.py
# 
# ============================================================================

from gtts import gTTS
import io
from pydub import AudioSegment
from pydub.playback import play
from .runtime_test import LogExecutionTime

class TTS_move:
    """
    A class to convert text strings, especially chess moves, to speech using Google's Text-to-Speech (TTS) service.

    This class is designed to take chess move strings in Universal Chess Interface (UCI) format and convert them 
    into spoken words for audible feedback. It supports promotion moves by expanding UCI notation into a more 
    understandable spoken format.

    Methods:
        speech (text_str): Converts a UCI format string into speech.
    """

    def __init__(self):
        """
        Initializes the TTS_move class.
        """
        pass

    @LogExecutionTime
    def speech(self, text_str):
        """
        Converts a given text string, particularly a chess move, into spoken words.

        The method takes a UCI formatted chess move and converts it into a more human-friendly spoken format.
        It handles both regular and promotion moves. For promotion moves, it explicitly states the piece to 
        which the pawn is promoted.

        Args:
            text_str (str): A string representing a chess move in UCI format.

        Returns:
            None: The method plays the converted speech audio but does not return any value.
        """
        language = 'en'
        promotion  = {"n": "knight", "q": "queen", "b": "bishop", "p": "pawn"}
        
        # Convert UCI formatted string to a more understandable spoken format
        if len(text_str) == 5:
            tts_formatting = text_str[:2] + " to " + text_str[2:4] + " promote to " + promotion[text_str[-1]]
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
