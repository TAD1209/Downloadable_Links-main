import json
import time
import os
import requests
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

VIDEO_URL = "https://monticello.viebit.com/watch?hash=HCZTN4vuyJ91LlrS"
SEGMENT_PREFIX = "pc20250401"
MAX_SEGMENTS = 300

def get_driver():
    options = Options()
    options.add_argument("--user-data-dir=C:/tmp/ChromeProfile")  # Use your profile
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    return webdriver.Chrome(options=options)

def get_segment_base_url(driver):
    driver.get(VIDEO_URL)
    input("[!] Let the video load, then press ENTER...")

    logs = driver.get_log("performance")
    for entry in logs:
        try:
            msg = json.loads(entry["message"])
            url = msg["message"]["params"]["request"]["url"]
            if ".fmp4" in url and SEGMENT_PREFIX in url:
                print(f"[✓] Found base URL: {url}")
                return url.rsplit("-", 1)[0] + "-"
        except:
            continue
    raise Exception("No .fmp4 segment found.")

def get_session_cookies(driver):
    session = requests.Session()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])
    return session

def download_segments(session, base_url, start=1, max_segments=300):
    os.makedirs("segments", exist_ok=True)
    merge_list = []

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": VIDEO_URL,
        "Accept": "*/*",
        "Origin": "https://monticello.viebit.com"
    }

    for i in range(start, start + max_segments):
        segment_url = f"{base_url}{i}.fmp4?fmp4=1"
        seg_path = f"segments/seg_{i}.fmp4"
        print(f"[↓] Downloading segment {i}...")
        try:
            r = session.get(segment_url, headers=headers, timeout=10)
            if r.status_code == 200:
                with open(seg_path, "wb") as f:
                    f.write(r.content)
                merge_list.append(f"file '{seg_path}'")
            else:
                print(f"[✗] Segment {i} failed: {r.status_code}")
                if r.status_code == 418:
                    print("[!] 418 means bot protection is still active. Trying more headers or referer may help.")
                break
        except Exception as e:
            print(f"[✗] Segment {i} error: {e}")
            break
    return merge_list


def merge_with_ffmpeg(merge_list):
    with open("merge_list.txt", "w") as f:
        f.write("\n".join(merge_list))
    subprocess.run([
        "ffmpeg", "-f", "concat", "-safe", "0",
        "-i", "merge_list.txt", "-c", "copy", "final_video.mp4"
    ])
    print("[✅] Video saved as final_video.mp4")

if __name__ == "__main__":
    driver = get_driver()
    try:
        base_url = get_segment_base_url(driver)
        session = get_session_cookies(driver)
        merge_list = download_segments(session, base_url)
        if merge_list:
            merge_with_ffmpeg(merge_list)
        else:
            print("[!] No valid segments downloaded.")
    finally:
        driver.quit()
