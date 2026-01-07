import pyttsx3
import os

def text_to_speech_file(text, folder):
    engine = pyttsx3.init()

    # 🔊 Available voices get karo
    voices = engine.getProperty('voices')

    #  Female voice select karo (usually index 1 is female on Windows)
    for voice in voices:
        if "female" in voice.name.lower() or "zira" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    else:
        # fallback (index 1)
        if len(voices) > 1:
            engine.setProperty('voice', voices[1])

    engine.setProperty('rate', 155)   # speed (female voice me smooth)
    engine.setProperty('volume', 1.0) # max volume

    output_path = f"user_uploads/{folder}/audio.mp3"
    engine.save_to_file(text, output_path)
    engine.runAndWait()
