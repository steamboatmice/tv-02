import time
import re
import requests
from http.server import BaseHTTPRequestHandler
import json
from .config import CHANNELS, USER_AGENT, TIMEOUT, CACHE_DURATION

# Simple In-Memory Cache
_cache = {}

def get_cached_url(channel_id):
    global _cache
    now = time.time()
    if channel_id in _cache:
        data, expiry = _cache[channel_id]
        if now < expiry:
            return data
    return None

def set_cached_url(channel_id, url):
    global _cache
    _cache[channel_id] = (url, time.time() + CACHE_DURATION)

def scrape_stream_url(channel_id):
    """
    Scrapes the stream URL using the configuration for the given channel_id.
    """
    conf = CHANNELS.get(channel_id)
    if not conf:
        return None
    
    cached = get_cached_url(channel_id)
    if cached:
        return cached

    headers = {
        "User-Agent": USER_AGENT,
        "Referer": conf["referer"],
        "Origin": conf["referer"]
    }
    
    try:
        response = requests.get(conf["url"], headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        
        match = re.search(conf["regex"], response.text, re.IGNORECASE)
        if match:
            found_url = match.group(1).replace('\\/', '/')
            set_cached_url(channel_id, found_url)
            return found_url
            
    except Exception as e:
        print(f"Error scraping {channel_id}: {e}")
    
    # Return fallback if available
    return conf.get("fallback")

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split('?')[0].rstrip('/')
        
        if path == "" or path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("IPTV Proxy Active. Usage: /playlist.m3u".encode('utf-8'))
            return

        if path == "/playlist.m3u":
            self.handle_playlist()
            return

        # Handle individual channels
        channel_id = path.lstrip('/')
        if channel_id in CHANNELS:
            stream_url = scrape_stream_url(channel_id)
            if stream_url:
                self.send_response(302)
                self.send_header('Location', stream_url)
                self.end_headers()
            else:
                self.send_error(404, f"Link for {channel_id} not found")
        else:
            self.send_error(404, "Not Found")

    def handle_playlist(self):
        # Protocols/Hosts detection for Vercel
        host = self.headers.get('Host', 'localhost')
        protocol = self.headers.get('X-Forwarded-Proto', 'https') # Vercel usually provides this
        base_url = f"{protocol}://{host}"

        m3u = ["#EXTM3U"]
        
        # Sort channels by group then name
        sorted_channels = sorted(CHANNELS.items(), key=lambda x: (x[1]['group'], x[1]['name']))
        
        for cid, info in sorted_channels:
            m3u.append(f'#EXTINF:-1 group-title="{info["group"]}" tvg-logo="{info["logo"]}",{info["name"]}')
            # Optimization tag for VLC as per project-context.md
            m3u.append("#EXTVLCOPT:adaptive-max-bandwidth=2000000")
            m3u.append(f"{base_url}/{cid}")
            m3u.append("")

        content = "\n".join(m3u)
        self.send_response(200)
        self.send_header('Content-id', 'audio/x-mpegurl')
        self.send_header('Content-Type', 'audio/x-mpegurl; charset=utf-8')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

# Local testing
if __name__ == "__main__":
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 8080), handler)
    print("Server started at http://localhost:8080")
    server.serve_forever()