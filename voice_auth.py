import speech_recognition as sr
from gtts import gTTS
import tempfile
import os
import time
from playsound import playsound

def convert_digits_to_words(digits):
    digit_map = {
        '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
        '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'
    }
    return ' '.join(digit_map.get(d, '') for d in digits)

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = r.listen(source, timeout=5)
            return r.recognize_google(audio)
        except Exception:
            return None

def recognize_operation():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio, language='hi-IN').lower()

            if any(k in text for k in ["balance", "बैलेंस", "ಬ್ಯಾಲೆನ್ಸ್"]):
                return "Balance Enquiry"
            elif any(k in text for k in ["deposit", "जमा", "ಹಣ ಠೇವಣಿ"]):
                return "Deposit"
            elif any(k in text for k in ["withdraw", "निकासी", "ಹಣ ವಾಪಸಾತಿ"]):
                return "Withdraw"
            elif any(k in text for k in ["passbook", "statement", "पासबुक", "ಪಾಸ್‌ಬುಕ್"]):
                return "Passbook"
            elif any(k in text for k in ["exit", "quit", "बंद", "ಹಾರಿ"]):
                return "Exit"
            else:
                return None
        except Exception:
            return None

def speak_text(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name
            tts.save(temp_path)
        playsound(temp_path)
        time.sleep(0.5)
        os.remove(temp_path)
    except Exception as e:
        print("TTS Error:", e)
