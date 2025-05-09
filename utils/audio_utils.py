# utils/audio_utils.py

import os
from gtts import gTTS
import pygame
import time

def create_audio(text, lang='en'):
    """Convert text to speech and save it as an audio file."""
    audio_path = "output.mp3"
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(audio_path)
    return audio_path

def play_audio(audio_path):
    """Play the audio file."""
    # Initialize pygame mixer for audio playback
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()
    
    # Wait until the audio finishes playing
    while pygame.mixer.music.get_busy():  # Check if the music is still playing
        time.sleep(0.1)
