from text_to_audio import text_to_audio
import os
import time
import subprocess

def create_reel(folder):
    os.makedirs("static/reels", exist_ok=True)

    cmd = (
        f'ffmpeg -f concat -safe 0 -i user_uploads/{folder}/input.txt '
        f'-i user_uploads/{folder}/audio.mp3 '
        f'-vf "scale=1080:1920:force_original_aspect_ratio=decrease,'
        f'pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" '
        f'-c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p '
        f'static/reels/{folder}.mp4'
    )
    subprocess.run(cmd, shell=True)
    print("CR -", folder)

if __name__ == "__main__":
    if not os.path.exists("done.txt"):
        open("done.txt", "w").close()

    while True:
        print("Processing queue...")

        with open("done.txt") as f:
            done = set(x.strip() for x in f.readlines())

        for folder in os.listdir("user_uploads"):
            if folder in done:
                continue

            print("New folder:", folder)
            try:
                if text_to_audio(folder):
                    create_reel(folder)
            except Exception as e:
                print("Error:", e)

            with open("done.txt", "a") as f:
                f.write(folder + "\n")

            time.sleep(2)

        time.sleep(4)
