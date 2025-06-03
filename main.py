from flask import Flask, request, jsonify
import os
import uuid
import subprocess

app = Flask(__name__)

# مجلد التحميل
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# راوت الفحص
@app.route("/", methods=["GET"])
def index():
    return "yt-dlp server is running!"

# راوت التحميل
@app.route("/download", methods=["POST"])
def download_video():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "Missing URL"}), 400

    # توليد اسم عشوائي للملف
    unique_id = str(uuid.uuid4())
    output_path = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}.mp3")

    # تحميل الفيديو بصيغة MP3
    try:
        subprocess.run([
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "-o", output_path,
            url
        ], check=True)

        return jsonify({"download_url": f"/{output_path}"})
    except subprocess.CalledProcessError:
        return jsonify({"error": "Download failed"}), 500