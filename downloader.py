import yt_dlp

def download_mp3(url, output_path="downloads"):
    opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_path}/%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }],
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return info["requested_downloads"][0]["filepath"]

def download_mp4(url, output_path="downloads"):
    opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": f"{output_path}/%(title)s.%(ext)s",
        "merge_output_format": "mp4",
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return info["requested_downloads"][0]["filepath"]

def _collect_filepaths(info):
    filepaths = []
    for entry in info.get("entries", []):
        if entry:
            for dl in entry.get("requested_downloads", []):
                if "filepath" in dl:
                    filepaths.append(dl["filepath"])
    return filepaths

def download_playlist_mp3(url, output_path="downloads"):
    opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_path}/%(playlist_title)s/%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }],
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return info.get("title", "playlist"), _collect_filepaths(info)

def download_playlist_mp4(url, output_path="downloads"):
    opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": f"{output_path}/%(playlist_title)s/%(title)s.%(ext)s",
        "merge_output_format": "mp4",
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return info.get("title", "playlist"), _collect_filepaths(info)