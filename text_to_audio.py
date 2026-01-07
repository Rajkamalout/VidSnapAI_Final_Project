import pyttsx3
import os

engine = pyttsx3.init()
engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)

def text_to_audio(folder):
    print("TTA -", folder)

    desc_path = f"user_uploads/{folder}/desc.txt"
    if not os.path.exists(desc_path):
        print("desc.txt not found:", folder)
        return False

    # READ AS BYTES (NO UTF ERROR)
    with open(desc_path, "rb") as f:
        raw = f.read()

    try:
        text = raw.decode("utf-8").strip()
    except UnicodeDecodeError:
        text = raw.decode("cp1252", errors="ignore").strip()

    if not text:
        print("desc.txt empty:", folder)
        return False

    output_path = f"user_uploads/{folder}/audio.mp3"
    engine.save_to_file(text, output_path)
    engine.runAndWait()

    print("Audio saved:", output_path)
    return True
