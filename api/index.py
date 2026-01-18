from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
import requests
import re

# --- AYARLAR ---
TIMEOUT = 10
# Bu User-Agent "Ben en güncel Chrome tarayıcısıyım" der.
UA_STRING = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

HEADERS = {
    "User-Agent": UA_STRING,
    "Referer": "https://www.google.com/"
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
            self.wfile.write("<h1>Sistem Aktif!</h1><p>Link: <a href='/playlist.m3u'>/playlist.m3u</a></p>".encode())
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
            r = requests.get(url, headers={"User-Agent": HEADERS["User-Agent"], "Referer": referer}, timeout=TIMEOUT)
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
        
        # VLC ve Akıllı TV'ler için "Kimlik Bilgisi" (EXTVLCOPT) ekliyoruz
        # Bu satırlar oynatıcıya "Videoyu çekerken bu kimliği kullan" der.
        m3u = f"""#EXTM3U
#EXTINF:-1 group-title="Ulusal",NOW TV
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.nowtv.com.tr/
{base}/now

#EXTINF:-1 group-title="Ulusal",ATV
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.atv.com.tr/
{base}/atv

#EXTINF:-1 group-title="Ulusal",Show TV
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.showtv.com.tr/
{base}/show

#EXTINF:-1 group-title="Ulusal",Star TV
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.startv.com.tr/
{base}/star

#EXTINF:-1 group-title="Haber",A Haber
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.ahaber.com.tr/
{base}/ahaber

#EXTINF:-1 group-title="Ulusal",TRT 1
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.trt.com.tr/
{base}/trt1
"""
        self.send_response(200)
        self.send_header('Content-type', 'audio/x-mpegurl') # Dosya türünü M3U olarak tanıttık
        self.end_headers()
        self.wfile.write(m3u.encode('utf-8'))
