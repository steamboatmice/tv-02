from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
import requests
import re

# --- AYARLAR ---
TIMEOUT = 10
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.google.com/"
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Gelen isteğin adresini al (/now, /atv vs.)
        path = urlparse(self.path).path
        
        # --- YÖNLENDİRME MANTIĞI ---
        redirect_url = None
        
        if path == '/now':
            redirect_url = self.get_stream("https://www.nowtv.com.tr/canli-yayin", "https://www.nowtv.com.tr/", r"daionUrl\s*:\s*.*?'(https://.*?\.m3u8.*?)'")
        
        elif path == '/atv':
            redirect_url = self.get_stream("https://www.atv.com.tr/canli-yayin", "https://www.atv.com.tr/", r"[\"'](https://.*?atv.*?\.m3u8.*?)[\"']")
            if not redirect_url: redirect_url = "https://tmgrup.daioncdn.net/atv/atv.m3u8"

        elif path == '/show':
            redirect_url = self.get_stream("https://www.showtv.com.tr/canli-yayin", "https://www.showtv.com.tr/", r"[\"'](https://.*?showtv.*?\.m3u8.*?)[\"']")
            if not redirect_url: redirect_url = "https://ciner-live.daioncdn.net/showtv/showtv.m3u8"
            
        elif path == '/ahaber':
            redirect_url = self.get_stream("https://www.ahaber.com.tr/video/canli-yayin", "https://www.ahaber.com.tr/", r"[\"'](https://.*?ahaber.*?\.m3u8.*?)[\"']")
            if not redirect_url: redirect_url = "https://tmgrup.daioncdn.net/ahaber/ahaber.m3u8"

        elif path == '/trt1':
            redirect_url = self.get_stream("https://www.tabii.com/tr/watch/live/trt1?trackId=150002", "https://www.tabii.com/", r"[\"'](https://.*?trt1.*?\.m3u8.*?)[\"']")
            if not redirect_url: redirect_url = "https://tv-trt1.medya.trt.com.tr/master.m3u8"
            
        elif path == '/star':
            redirect_url = self.get_stream("https://www.startv.com.tr/canli-yayin", "https://www.startv.com.tr/", r"[\"'](https://.*?startv.*?\.m3u8.*?)[\"']")
            if not redirect_url: redirect_url = "https://dogus-live.daioncdn.net/startv/startv.m3u8"

        elif path == '/playlist.m3u':
            self.send_playlist()
            return

        elif path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("<h1>Sistem (Saf Python) Calisiyor!</h1><p>Link: <a href='/playlist.m3u'>/playlist.m3u</a></p>".encode())
            return
        
        else:
            self.send_error(404, "Kanal Bulunamadi")
            return

        # --- SONUÇ: EĞER LİNK BULUNDUYSA YÖNLENDİR ---
        if redirect_url:
            self.send_response(302)
            self.send_header('Location', redirect_url)
            self.end_headers()
        else:
            self.send_error(404, "Yayin Linki Cekilemedi")

    # --- YARDIMCI FONKSİYONLAR ---
    def get_stream(self, url, referer, regex):
        try:
            r = requests.get(url, headers={"User-Agent": HEADERS["User-Agent"], "Referer": referer}, timeout=TIMEOUT)
            match = re.search(regex, r.text)
            if match:
                return match.group(1).replace('\\/', '/')
        except:
            pass
        return None

    def send_playlist(self):
        # Host adresini otomatik bul (http/https fark etmez)
        host = self.headers.get('Host')
        protocol = "https" if "localhost" not in host else "http"
        base = f"{protocol}://{host}"
        
        m3u = f"""#EXTM3U
#EXTINF:-1 group-title="Ulusal",NOW TV
{base}/now
#EXTINF:-1 group-title="Ulusal",ATV
{base}/atv
#EXTINF:-1 group-title="Ulusal",Show TV
{base}/show
#EXTINF:-1 group-title="Ulusal",Star TV
{base}/star
#EXTINF:-1 group-title="Haber",A Haber
{base}/ahaber
#EXTINF:-1 group-title="Ulusal",TRT 1
{base}/trt1
"""
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(m3u.encode('utf-8'))
