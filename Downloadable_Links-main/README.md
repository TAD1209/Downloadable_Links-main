# 🎥 m3u8 Video Scraper and Downloader

This Python project automates the extraction and downloading of `.m3u8` video streams from dynamic JavaScript-heavy websites using **Selenium** and **yt-dlp**. It's useful for capturing live or archived video streams that are not directly downloadable via right-click or inspect tools.

---

## ⚙️ Features

- Extracts all `.m3u8` links from dynamic web pages
- Automatically downloads videos using `yt-dlp` with proper headers
- Supports sites like ChampDS, VieBit, and IBM Cloud Video

---

## 🔧 Requirements

- Python **3.7+** (tested up to 3.13)
- Google Chrome installed
- ChromeDriver (matching your Chrome version) in your system PATH
- `yt-dlp` (installed via pip)

---

## 📦 Installation

1. Clone or download this repository.
2. Install dependencies:

```bash
pip install -r requirements.txt

