from flask import Flask, request, jsonify
import os
import subprocess
import uuid

app = Flask(__name__)

# 1. مجلد التحميلات
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# 2. راوت فحص السيرفر
@app.route("/", methods=["GET"])
def index():
    return "yt-dlp server is running!"

# 3. راوت التحميل
@app.route("/download", methods=["POST"])
def download_video():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "Missing URL"}), 400

    unique_id = str(uuid.uuid4())
    output_path = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}.mp3")

    # 4. تحميل وتحويل mp3
    try:
        subprocess.run([
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "-o", output_path,
            url
        ], check=True)

        return jsonify({
            "download_url": f"/{output_path}"
        })
    except subprocess.CalledProcessError:
        return jsonify({"error": "Download failed"}), 500

# 5. تشغيل السيرفر
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)