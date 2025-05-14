import os
import subprocess
from datetime import datetime
import pytz
from flask import Flask

app = Flask(__name__)

def capture_snapshots():
    timezone = pytz.timezone("Europe/Warsaw")
    now = datetime.now(timezone)
    date_str = now.strftime("%m-%d")
    time_str = now.strftime("%H%M")

    streams = {
        "Twitch_Gdansk": "https://www.twitch.tv/alokum_nieruchomosci",
        "YT_Poland": "https://www.youtube.com/watch?v=S2L-hzuRX0g",
        "YT_Mechelen1": "https://www.youtube.com/watch?v=xQKCnSsATK0",
        "YT_Mechelen2": "https://www.youtube.com/watch?v=m5HWzP2wNGE",
        "YT_Lokeren": "https://www.youtube.com/watch?v=HUeaYuBLNNQ"
    }

    cookies_path = "cookies.txt"  # Include this in your Git repo

    for name, url in streams.items():
        folder = os.path.join("snapshots", name, date_str)
        os.makedirs(folder, exist_ok=True)
        output_path = os.path.join(folder, f"{time_str}.jpg")

        if "youtube" in url:
            command = f"yt-dlp --cookies {cookies_path} -f best -o - \"{url}\" | ffmpeg -loglevel error -y -i - -frames:v 1 \"{output_path}\""
        else:
            command = f"yt-dlp -f best -o - \"{url}\" | ffmpeg -loglevel error -y -i - -frames:v 1 \"{output_path}\""

        print(f"[{name}] Capturing frame at {date_str} {time_str}...")
        subprocess.call(command, shell=True)

    print("Uploading to cloud...")
    subprocess.call("rclone copy snapshots remote:LivestreamSnapshots", shell=True)
    print("Upload complete.")

@app.route('/')
def home():
    return "Use /run to trigger snapshot."

@app.route('/run')
def run():
    capture_snapshots()
    return "Snapshots captured."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
