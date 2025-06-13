import subprocess

def download_ibm_video_with_ytdlp(page_url,  output_file="output.mp4"):
    command = [
        "yt-dlp",
        "-o", output_file,
        page_url
    ]

    print(f"[>] Running: {' '.join(command)}")
    result = subprocess.run(command)

    if result.returncode == 0:
        print("[✓] Download completed successfully!")
    else:
        print("[✗] yt-dlp failed. Check cookies or page URL.")

if __name__ == "__main__":
    video_url = "https://video.ibm.com/recorded/134312408"
    download_ibm_video_with_ytdlp(video_url, output_file="lecture.mp4")