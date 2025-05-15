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
        "Twitch_Gdansk":       "https://www.twitch.tv/alokum_nieruchomosci",
        "Twitch_Paris":        "https://www.twitch.tv/paris_webcam",
        "Twitch_Petersberg":   "https://www.twitch.tv/mobotixwebcamsrussia",
        "Twitch_Tokyo":        "https://www.twitch.tv/edoriver365",
        "Twitch_Groningen":    "https://www.twitch.tv/webcamoostersluis",
        "Twitch_Zandvoort":    "https://www.twitch.tv/webcamzandvoort",
        "Twitch_Scotland_Bay": "https://www.twitch.tv/cmalcastlebay",
        "Twitch_Scotland_Isle":"https://www.twitch.tv/cmalbrodick",
        "Twitch_Massachusetts":"https://www.twitch.tv/patobrienassoc_mi"
    }

    for name, url in streams.items():
        folder = os.path.join("snapshots", name, date_str)
        os.makedirs(folder, exist_ok=True)
        output_path = os.path.join(folder, f"{time_str}.jpg")

        # Use yt-dlp + ffmpeg to grab one frame
        cmd = (
            f'yt-dlp -f best -o - "{url}" '
            f'| ffmpeg -loglevel error -y -i - -frames:v 1 "{output_path}"'
        )
        print(f"[{name}] Capturing frame at {date_str} {time_str}…")
        subprocess.call(cmd, shell=True)

    # Upload to Google Drive (via rclone)
    print("Uploading to Google Drive…")
    rclone_config = os.getenv("RCLONE_CONFIG")
    if rclone_config:
        with open("/app/rclone.conf", "w") as f:
            f.write(rclone_config)
        subprocess.call(
            "rclone copy snapshots gdrive:LivestreamSnapshots --config /app/rclone.conf",
            shell=True
        )
        print("Upload complete.")
    else:
        print("RCLONE_CONFIG not found; skipping upload.")

@app.route('/')
def home():
    return "Snapshot service is running. Call /run to take snapshots."

@app.route('/run')
def run():
    capture_snapshots()
    return "Snapshots captured."

if __name__ == '__main__':
    # Render will keep this web process alive
    app.run(host='0.0.0.0', port=10000)
