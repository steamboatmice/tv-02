import requests
import time

BASE_URL = "http://localhost:8080"

def test_root():
    print("Testing root...")
    resp = requests.get(BASE_URL)
    print(f"Status: {resp.status_code}, Content: {resp.text}")

def test_playlist():
    print("\nTesting playlist...")
    resp = requests.get(f"{BASE_URL}/playlist.m3u")
    print(f"Status: {resp.status_code}")
    if "#EXTM3U" in resp.text:
        print("Playlist is valid M3U")
    else:
        print("Playlist is INVALID")

def test_channels():
    channels = ["now", "atv", "trt1"]
    for ch in channels:
        print(f"\nTesting channel: {ch}...")
        resp = requests.get(f"{BASE_URL}/{ch}", allow_redirects=False)
        print(f"Status: {resp.status_code}, Location: {resp.headers.get('Location')}")

if __name__ == "__main__":
    # Note: You need to run the server first: python api/index.py
    # This script assumes the server is running.
    try:
        test_root()
        test_playlist()
        test_channels()
    except Exception as e:
        print(f"Test failed: {e}")
