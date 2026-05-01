import os
import re
import zipfile
import tempfile
import shutil
from urllib.parse import quote
from flask import Flask, request, send_from_directory, send_file, after_this_request
from flask_cors import CORS
from downloader import download_mp3, download_mp4, download_playlist_mp3, download_playlist_mp4

app = Flask(__name__)
CORS(app, expose_headers=["X-Filename"])

def safe_filename(filename):
    return re.sub(r'[\x00-\x1F\x7F]', '', filename).strip()

def build_file_response(filepath):
    filename = os.path.basename(filepath)
    
    @after_this_request
    def cleanup(response):
        try:
            os.remove(filepath)
        except Exception as e:
            app.logger.warning(f"Could not delete {filepath}: {e}")
        return response
    
    file_obj = send_file(filepath, as_attachment=True)
    file_obj.headers["X-Filename"] = quote(safe_filename(filename))
    return file_obj

def build_playlist_response(playlist_title, filepaths):
    safe_title = safe_filename(playlist_title) or "playlist"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".zip", prefix=safe_title + "_")
    tmp.close()
    with zipfile.ZipFile(tmp.name, "w", zipfile.ZIP_DEFLATED) as zf:
        for fp in filepaths:
            zf.write(fp, os.path.basename(fp))

    @after_this_request
    def cleanup(response):
        for fp in filepaths:
            folder = os.path.dirname(fp)
            try:
                shutil.rmtree(folder)
            except Exception:
                pass
        try:
            os.remove(tmp.name)
        except Exception:
            pass
        return response

    file_obj = send_file(tmp.name, as_attachment=True)
    file_obj.headers["X-Filename"] = quote(safe_title + ".zip")
    return file_obj

@app.route("/playlist-mp3", methods=["POST"])
def playlist_audio():
    url = (request.get_json() or {}).get("url")
    if not url:
        return {"error": "Missing url"}, 400
    title, filepaths = download_playlist_mp3(url)
    return build_playlist_response(title, filepaths)

@app.route("/playlist-mp4", methods=["POST"])
def playlist_video():
    url = (request.get_json() or {}).get("url")
    if not url:
        return {"error": "Missing url"}, 400
    title, filepaths = download_playlist_mp4(url)
    return build_playlist_response(title, filepaths)

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/mp3", methods=["POST"])
def audio():
    url = (request.get_json() or {}).get("url")
    if not url:
        return {"error": "Missing url"}, 400
    return build_file_response(download_mp3(url))

@app.route("/mp4", methods=["POST"])
def video():
    url = (request.get_json() or {}).get("url")
    if not url:
        return {"error": "Missing url"}, 400
    return build_file_response(download_mp4(url))

@app.route("/LICENSE")
def license():
    return send_from_directory(".", "LICENSE")

if __name__ == "__main__":
    app.run(
        host='0.0.0.0', 
        port=5000, 
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true"
    )
