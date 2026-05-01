const input = document.getElementById("input")
const submitBtn = document.getElementById("submit");
const form = document.querySelector("form");
const videoAudioToggle = document.getElementById("video-audio-toggle");

let downloadVideo = true;

videoAudioToggle.addEventListener("click", () => {
    if(downloadVideo) {
        downloadVideo = false;
        videoAudioToggle.textContent = "Audio";
    }
    else {
        downloadVideo = true;
        videoAudioToggle.textContent = "Video";
    }
});

const YT_URL_RE = /^https?:\/\/((www\.|music\.)?youtube\.com\/(watch\?.*v=|shorts\/|playlist\?.*list=)|youtu\.be\/)[-\w]+/;
const YT_PLAYLIST_RE = /[?&]list=[-\w]+/;

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const url = input.value.trim();
    if (!YT_URL_RE.test(url)) {
        alert("Please enter a valid YouTube URL.");
        return;
    }

    const fileFormat = downloadVideo ? "mp4" : "mp3";
    const isPlaylist = url.includes("playlist?list=") || (YT_PLAYLIST_RE.test(url) && !url.includes("/shorts/"));
    const endpoint = isPlaylist ? `playlist-${fileFormat}` : fileFormat;

    submitBtn.disabled = true;
    videoAudioToggle.disabled = true;
    submitBtn.innerHTML = '<div class="spinner"></div> Downloading';

    try {
        const response = await fetch(`/${endpoint}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url })
        });

        if (!response.ok) {
            const data = await response.json().catch(() => ({}));
            alert(data.error || "Download failed.");
            return;
        }

        const filename = decodeURIComponent(response.headers.get("X-Filename") || "");
        const blob = await response.blob();
        const downloadUrl = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = downloadUrl;
        a.download = filename || `file.${isPlaylist ? "zip" : fileFormat}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(downloadUrl);
    } finally {
        submitBtn.disabled = false;
        videoAudioToggle.disabled = false;
        submitBtn.textContent = 'Download';
        input.value = '';
    }
});