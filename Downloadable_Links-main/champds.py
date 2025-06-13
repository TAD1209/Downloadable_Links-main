import json
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def extract_all_m3u8_urls(page_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(page_url)

    print("[*] Waiting for network activity...")
    time.sleep(10)

    logs = driver.get_log("performance")
    driver.quit()

    m3u8_urls = set()  # Use a set to avoid duplicates

    for entry in logs:
        try:
            message = json.loads(entry["message"])
            url = message["message"]["params"]["request"]["url"]
            if ".m3u8" in url:
                m3u8_urls.add(url)
        except Exception:
            continue

    return list(m3u8_urls)

def download_m3u8_with_headers(m3u8_url, referer):
    command = [
        "yt-dlp",
        "--add-header", "User-Agent: Mozilla/5.0",
        "--add-header", f"Referer: {referer}",
        m3u8_url
    ]
    print(f"[>] Running: {' '.join(command)}")
    subprocess.run(command)

if __name__ == "__main__":
    page_url = "https://play.champds.com/guilderlandny/event/431"

    m3u8_urls = extract_all_m3u8_urls(page_url)

    if m3u8_urls:
        print("\n[+] Downloadable .m3u8 URLs found:")
        for i, url in enumerate(m3u8_urls, 1):
            print(f"{i}. {url}")

        print("\n[*] Starting download for each link...\n")
        for m3u8_url in m3u8_urls:
            download_m3u8_with_headers(m3u8_url, referer=page_url)
    else:
        print("[-] Failed to find any .m3u8 URLs.")
