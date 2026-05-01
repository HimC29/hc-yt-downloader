<div align="center">

# 📥 HC-YT Downloader

### A Self-Hosted Web App to Download YouTube Videos & Audio

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-yellow.svg?style=for-the-badge)](https://opensource.org/license/gpl-3.0)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Server-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=yellow)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

**A lightweight, self-hosted YouTube downloader with a clean web UI — paste a URL, pick video or audio, and download. No ads, no tracking, no nonsense.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [How It Works](#-how-it-works) • [Project Structure](#-project-structure) • [Contributing](#-contributing)

</div>

---

## ✨ Features

<table>
<tr>
<td>

📥 **Video & Audio**  
Download as MP4 or extract audio as MP3

🔗 **Broad URL Support**  
Works with `youtube.com`, `youtu.be`, `music.youtube.com`, and `/shorts/`

⚡ **Lightweight**  
No frontend framework — pure vanilla JS, HTML, and CSS

</td>
<td>

🎨 **Clean UI**  
Minimal dark-themed interface with a download spinner

🗑 **Auto Cleanup**  
Downloaded files are deleted from the server after being sent

🔒 **Local Only**  
Runs entirely on your machine — nothing leaves your network

</td>
</tr>
</table>

---

## 🤔 Why This Project?

Most YouTube downloaders are either bloated with ads, require browser extensions, or are shady websites that can't be trusted. This project gives you a clean, self-hosted alternative you can run locally in seconds.

- 🚫 **No ads or tracking** — it's just a local web server
- 🛠 **Full control** — open source, you can see exactly what it does
- ⚡ **One paste, one click** — paste URL, choose format, download
- 🧠 **Learning project** — built to learn Flask and yt-dlp

---

## 🚀 Installation

### Prerequisites

- Python 3.8+
- [FFmpeg](https://ffmpeg.org/download.html) (required for MP3 extraction and MP4 merging)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/HimC29/hc-yt-downloader.git
   cd hc-yt-downloader
   ```

2. **Install dependencies**
   ```bash
   pip install flask flask-cors yt-dlp
   ```

3. **Run the server**
   ```bash
   python server.py
   ```

4. **Open in your browser**  
   Navigate to `http://localhost:5000`

> ⚠️ **Note:** This uses Flask's built-in development server, which is intended for local use only. Do not expose it to the public internet.

---

## 📖 Usage

1. Paste a YouTube URL into the input field  
   *(supports `youtube.com/watch`, `youtu.be`, `music.youtube.com`, and `youtube.com/shorts`)*

2. Toggle between **Video** (MP4) and **Audio** (MP3) using the left button

3. Click **Download**

4. The file will be downloaded directly to your browser's downloads folder

---

## 🔧 How It Works

### Flow

```
Browser form submit
    └─► POST /mp4 or /mp3 (Flask)
            └─► yt-dlp downloads the file to /downloads
                    └─► Flask streams the file back to the browser
                            └─► File is deleted from server after sending
```

### Format Handling

- **MP4** — uses `bestvideo+bestaudio/best` and merges with FFmpeg
- **MP3** — uses `bestaudio/best` and extracts audio with FFmpeg's `FFmpegExtractAudio` postprocessor

### Filename

The original video title is used as the filename, passed back to the browser via the `X-Filename` response header.

---

## 📁 Project Structure

```
hc-yt-downloader/
├── server.py          — Flask server, routes, and file response logic
├── downloader.py      — yt-dlp download logic for MP3 and MP4
├── downloads/         — Temporary storage for downloaded files (auto-cleaned)
├── static/
│   ├── index.html     — Frontend UI
│   ├── main.js        — Form handling, fetch, and download trigger
│   ├── styles.css     — Dark-themed styling
│   └── media/
│       └── logo.svg   — App logo
├── LICENSE            — GPL v3 License
└── README.md          — Project documentation
```

---

## 🤝 Contributing

Contributions are welcome! If you find a bug or want to improve the app, feel free to open an issue or PR.

### How to Contribute

1. **Fork the Project**
2. **Create your Feature Branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your Changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the Branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Ideas for Contributions

- 🎨 Better UI / themes
- 📋 Download history log
- 🔔 Desktop notification on download complete
- 📂 Custom output directory support
- 🎞 Format/quality selector

---

## 🐛 Troubleshooting

### The page doesn't load
- Make sure the server is running with `python server.py`
- Check that you're navigating to `http://localhost:5000` (not `5001` or another port)

### "Please enter a valid YouTube URL"
- Make sure the URL starts with `https://`
- Supported formats: `youtube.com/watch?v=`, `youtu.be/`, `music.youtube.com/watch?v=`, `youtube.com/shorts/`

### Download fails or hangs
- Make sure FFmpeg is installed and available in your system PATH
- Try updating yt-dlp: `pip install -U yt-dlp`

---

## 📄 License

Distributed under the GPL v3 License. See [LICENSE](/LICENSE) for more information.

---

<div align="center">

### ⭐ Star this repo if you found it useful!

**Made with ♥️ by [HimC29](https://github.com/HimC29)**

[Report Bug](https://github.com/HimC29/hc-yt-downloader/issues) • [Request Feature](https://github.com/HimC29/hc-yt-downloader/issues)

</div>
