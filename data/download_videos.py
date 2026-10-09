"""
Traffic Video Downloader — Pexels API
======================================
Downloads traffic videos from Pexels based on predefined search queries.

Usage:
    python data/download_videos.py --api-key YOUR_PEXELS_API_KEY

Get your FREE API key at: https://www.pexels.com/api/
"""

import os
import sys
import argparse
import requests

# Video requirements: (filename, search_query, min_duration_sec)
VIDEO_SPECS = [
    ("traffic_01.mp4", "traffic intersection overhead",  30),
    ("traffic_02.mp4", "highway traffic cars trucks",     40),
    ("traffic_03.mp4", "busy city road traffic",          30),
    ("traffic_04.mp4", "traffic signal junction",         25),
    ("traffic_05.mp4", "quiet street low traffic",        30),
    ("traffic_06.mp4", "rain evening traffic city",       30),
    ("traffic_07.mp4", "mixed vehicles traffic road",     40),
]

SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw", "traffic_videos")

PEXELS_API_URL = "https://api.pexels.com/videos/search"


def search_videos(api_key: str, query: str, min_duration: int, per_page: int = 15):
    """Search Pexels for videos matching the query."""
    headers = {"Authorization": api_key}
    params = {
        "query": query,
        "orientation": "landscape",
        "per_page": per_page,
    }
    resp = requests.get(PEXELS_API_URL, headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    # Filter by duration and pick best candidate
    candidates = []
    for video in data.get("videos", []):
        duration = video.get("duration", 0)
        if duration >= min_duration:
            candidates.append(video)

    return candidates


def get_best_download_url(video: dict, min_width: int = 1280):
    """
    Pick the best video file (HD or above, mp4).
    Prefers smallest file that is >= min_width (720p = 1280 wide).
    """
    files = video.get("video_files", [])
    hd_files = [
        f for f in files
        if f.get("width", 0) >= min_width and f.get("file_type") == "video/mp4"
    ]
    if not hd_files:
        # Fallback: any mp4
        hd_files = [f for f in files if f.get("file_type") == "video/mp4"]

    if not hd_files:
        return None

    # Sort by width ascending, pick smallest HD
    hd_files.sort(key=lambda f: f.get("width", 9999))
    return hd_files[0].get("link")


def download_file(url: str, save_path: str):
    """Download a file with progress indicator."""
    print(f"  Downloading → {save_path}")
    resp = requests.get(url, stream=True, timeout=120)
    resp.raise_for_status()

    total = int(resp.headers.get("content-length", 0))
    downloaded = 0

    with open(save_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
            downloaded += len(chunk)
            if total > 0:
                pct = (downloaded / total) * 100
                print(f"\r  Progress: {pct:.1f}% ({downloaded // 1024} KB / {total // 1024} KB)", end="")

    print(f"\n  ✅ Saved: {save_path}\n")


def main():
    parser = argparse.ArgumentParser(description="Download traffic videos from Pexels")
    parser.add_argument("--api-key", required=True, help="Your Pexels API key")
    args = parser.parse_args()

    os.makedirs(SAVE_DIR, exist_ok=True)

    print("=" * 60)
    print("  Traffic Video Downloader — Pexels API")
    print("=" * 60)
    print(f"  Save directory: {SAVE_DIR}\n")

    success = 0
    failed = []

    for filename, query, min_dur in VIDEO_SPECS:
        save_path = os.path.join(SAVE_DIR, filename)

        # Skip if already downloaded
        if os.path.exists(save_path):
            print(f"⏩ {filename} already exists, skipping.")
            success += 1
            continue

        print(f"🔍 Searching: \"{query}\" (min {min_dur}s) → {filename}")

        try:
            candidates = search_videos(args.api_key, query, min_dur)
            if not candidates:
                print(f"  ❌ No suitable video found for \"{query}\"\n")
                failed.append(filename)
                continue

            # Try candidates in order
            downloaded = False
            for video in candidates[:3]:  # Try top 3 results
                url = get_best_download_url(video)
                if url:
                    download_file(url, save_path)
                    downloaded = True
                    success += 1
                    break

            if not downloaded:
                print(f"  ❌ Could not find HD download for \"{query}\"\n")
                failed.append(filename)

        except Exception as e:
            print(f"  ❌ Error: {e}\n")
            failed.append(filename)

    # Summary
    print("=" * 60)
    print(f"  DONE: {success}/{len(VIDEO_SPECS)} videos downloaded")
    if failed:
        print(f"  FAILED: {', '.join(failed)}")
        print("  → Please download these manually from Pexels/Pixabay")
    print("=" * 60)


if __name__ == "__main__":
    main()
