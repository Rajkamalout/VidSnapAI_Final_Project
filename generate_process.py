
import os
from text_to_audio import text_to_speech_file
import time
import subprocess


def text_to_audio(folder):
    print("TTA -", folder)

    desc_path = f"user_uploads/{folder}/desc.txt"
    if not os.path.exists(desc_path):
        print(" desc.txt not found:", folder)
        return False

    with open(desc_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print(" desc.txt empty:", folder)
        return False

    print(text, folder)
    text_to_speech_file(text, folder)
    return True


def create_reel(folder):
    output_dir = "static/reels"
    os.makedirs(output_dir, exist_ok=True)

    command = f'''ffmpeg -f concat -safe 0 -i user_uploads/{folder}/input.txt \
-i user_uploads/{folder}/audio.mp3 \
-vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
-c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p static/reels/{folder}.mp4'''

    subprocess.run(command, shell=True, check=True)
    print("CR -", folder)


if __name__ == "__main__":

    if not os.path.exists("done.txt"):
        open("done.txt", "w").close()

    while True:
        print("Processing queue...")

        with open("done.txt", "r") as f:
            done_folders = [line.strip() for line in f.readlines()]

        folders = os.listdir("user_uploads")

        for folder in folders:
            if folder not in done_folders:
                print(" New folder:", folder)

                if text_to_audio(folder):
                    create_reel(folder)

                    with open("done.txt", "a") as f:
                        f.write(folder + "\n")

                # SAFE delay (offline TTS so no issue)
                time.sleep(2)

        time.sleep(4)
