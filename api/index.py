from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
import requests
import re

# --- AYARLAR ---
TIMEOUT = 12
# Mobil Kamuflajı (Samsung S21) - Reklamları ve kesintileri önler
UA_STRING = "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36"

HEADERS = {
    "User-Agent": UA_STRING,
    "Referer": "https://www.nowtv.com.tr/",
    "Origin": "https://www.nowtv.com.tr",
    "Accept": "*/*",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        redirect_url = None
        
        # --- KANAL MANTIĞI ---
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
            self.wfile.write("<h1>Stabil Mod (Bitrate Limitli) Aktif!</h1><p>Link: <a href='/playlist.m3u'>/playlist.m3u</a></p>".encode())
            return
        
        else:
            self.send_error(404, "Kanal Bulunamadi")
            return

        # Yönlendirme
        if redirect_url:
            self.send_response(302)
            self.send_header('Location', redirect_url)
            self.end_headers()
        else:
            self.send_error(404, "Yayin Linki Cekilemedi")

    def get_stream(self, url, referer, regex):
        try:
            req_headers = HEADERS.copy()
            req_headers['Referer'] = referer
            r = requests.get(url, headers=req_headers, timeout=TIMEOUT)
            match = re.search(regex, r.text)
            if match:
                return match.group(1).replace('\\/', '/')
        except:
            pass
        return None

    def send_playlist(self):
        host = self.headers.get('Host')
        protocol = "https" if "localhost" not in host else "http"
        base = f"{protocol}://{host}"
        
        # --- BİTRATE KISITLAMA AYARLARI ---
        # 3500000 bps = Yaklaşık 3.5 Mbps (Genellikle 720p HD kalitesidir)
        # Bu ayar oynatıcıya "Daha yükseğine çıkma" der.
        
        m3u = f"""#EXTM3U
#EXTINF:-1 group-title="Ulusal",NOW TV (Stabil)
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.nowtv.com.tr/
#EXTVLCOPT:adaptive-max-bandwidth=3500000
#EXTVLCOPT:preferred-resolution=720
{base}/now

#EXTINF:-1 group-title="Ulusal",ATV (Stabil)
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.atv.com.tr/
#EXTVLCOPT:adaptive-max-bandwidth=3500000
#EXTVLCOPT:preferred-resolution=720
{base}/atv

#EXTINF:-1 group-title="Ulusal",Show TV (Stabil)
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.showtv.com.tr/
#EXTVLCOPT:adaptive-max-bandwidth=3500000
#EXTVLCOPT:preferred-resolution=720
{base}/show

#EXTINF:-1 group-title="Ulusal",Star TV (Stabil)
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.startv.com.tr/
#EXTVLCOPT:adaptive-max-bandwidth=3500000
#EXTVLCOPT:preferred-resolution=720
{base}/star

#EXTINF:-1 group-title="Haber",A Haber (Stabil)
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.ahaber.com.tr/
#EXTVLCOPT:adaptive-max-bandwidth=3500000
#EXTVLCOPT:preferred-resolution=720
{base}/ahaber

#EXTINF:-1 group-title="Ulusal",TRT 1 (Stabil)
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.trt.com.tr/
#EXTVLCOPT:adaptive-max-bandwidth=3500000
#EXTVLCOPT:preferred-resolution=720
{base}/trt1
"""
        self.send_response(200)
        self.send_header('Content-type', 'audio/x-mpegurl')
        self.end_headers()
        self.wfile.write(m3u.encode('utf-8'))
