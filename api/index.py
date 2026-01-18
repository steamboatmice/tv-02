from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
import requests
import re

# --- AYARLAR ---
TIMEOUT = 12
# Mobil Kamuflaj (Samsung S21) - Reklamları ve kesintileri önler
UA_STRING = "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36"

HEADERS = {
    "User-Agent": UA_STRING,
    "Referer": "https://www.google.com/",
    "Accept": "*/*",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        redirect_url = None
        
        # --- KANAL MANTIĞI ---
        
        # 1. NOW TV (Zaten çalışıyor, ellemedik)
        if path == '/now':
            redirect_url = self.get_stream("https://www.nowtv.com.tr/canli-yayin", "https://www.nowtv.com.tr/", r"daionUrl\s*:\s*.*?'(https://.*?\.m3u8.*?)'")
        
        # 2. ATV (Gelişmiş Tarama)
        elif path == '/atv':
            # ATV'nin orijinal sitesini tarar. 
            # Regex: Hem http hem https kabul eder, .m3u8 ile biten her şeyi yakalar.
            redirect_url = self.get_stream("https://www.atv.com.tr/canli-yayin", "https://www.atv.com.tr/", r"[\"'](https?://.*?\.m3u8.*?)[\"']")
            
            # Eğer siteden bulamazsa klasik tmgrup linkini kullanır (Bu link header ile çalışır)
            if not redirect_url: redirect_url = "https://tmgrup.daioncdn.net/atv/atv.m3u8"

        # 3. SHOW TV (Çalışıyor)
        elif path == '/show':
            redirect_url = self.get_stream("https://www.showtv.com.tr/canli-yayin", "https://www.showtv.com.tr/", r"[\"'](https?://.*?showtv.*?\.m3u8.*?)[\"']")
            if not redirect_url: redirect_url = "https://ciner-live.daioncdn.net/showtv/showtv.m3u8"
            
        # 4. A HABER (Gelişmiş Tarama)
        elif path == '/ahaber':
            redirect_url = self.get_stream("https://www.ahaber.com.tr/video/canli-yayin", "https://www.ahaber.com.tr/", r"[\"'](https?://.*?\.m3u8.*?)[\"']")
            if not redirect_url: redirect_url = "https://tmgrup.daioncdn.net/ahaber/ahaber.m3u8"

        # 5. TRT 1 (Tabii üzerinden)
        elif path == '/trt1':
            redirect_url = self.get_stream("https://www.tabii.com/tr/watch/live/trt1?trackId=150002", "https://www.tabii.com/", r"[\"'](https?://.*?trt1.*?\.m3u8.*?)[\"']")
            if not redirect_url: redirect_url = "https://tv-trt1.medya.trt.com.tr/master.m3u8"
            
        # 6. STAR TV
        elif path == '/star':
            redirect_url = self.get_stream("https://www.startv.com.tr/canli-yayin", "https://www.startv.com.tr/", r"[\"'](https?://.*?startv.*?\.m3u8.*?)[\"']")
            if not redirect_url: redirect_url = "https://dogus-live.daioncdn.net/startv/startv.m3u8"

        elif path == '/playlist.m3u':
            self.send_playlist()
            return

        elif path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("<h1>Orijinal Link Modu Aktif!</h1><p>Link: <a href='/playlist.m3u'>/playlist.m3u</a></p>".encode())
            return
        
        else:
            self.send_error(404, "Kanal Bulunamadi")
            return

        # Yönlendirme İşlemi
        if redirect_url:
            self.send_response(302)
            self.send_header('Location', redirect_url)
            self.end_headers()
        else:
            self.send_error(404, "Link Bulunamadi")

    # --- YARDIMCI FONKSİYONLAR ---
    def get_stream(self, url, referer, regex):
        try:
            # Headerları her istekte tazeleyerek gönderiyoruz
            req_headers = HEADERS.copy()
            req_headers['Referer'] = referer
            
            r = requests.get(url, headers=req_headers, timeout=TIMEOUT)
            
            # HTML içindeki linki regex ile ara
            match = re.search(regex, r.text)
            if match:
                found_url = match.group(1).replace('\\/', '/')
                
                # ÖNEMLİ DÜZELTME:
                # ATV bazen http link verir, modern oynatıcılar bunu engeller.
                # Biz zorla https yapıyoruz.
                if found_url.startswith("http://"):
                    found_url = found_url.replace("http://", "https://")
                
                return found_url
        except:
            pass
        return None

    def send_playlist(self):
        host = self.headers.get('Host')
        protocol = "https" if "localhost" not in host else "http"
        base = f"{protocol}://{host}"
        
        # OYNATICI AYARLARI (User-Agent ve Bitrate Limiti)
        # Turkuvaz grubu için Referer'ı "atv.com.tr" olarak zorluyoruz.
        
        m3u = f"""#EXTM3U
#EXTINF:-1 group-title="Ulusal",NOW TV
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.nowtv.com.tr/
#EXTVLCOPT:adaptive-max-bandwidth=3500000
#EXTVLCOPT:preferred-resolution=720
{base}/now

#EXTINF:-1 group-title="Ulusal",ATV
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.atv.com.tr/
#EXTVLCOPT:adaptive-max-bandwidth=3500000
#EXTVLCOPT:preferred-resolution=720
{base}/atv

#EXTINF:-1 group-title="Ulusal",Show TV
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.showtv.com.tr/
#EXTVLCOPT:adaptive-max-bandwidth=3500000
#EXTVLCOPT:preferred-resolution=720
{base}/show

#EXTINF:-1 group-title="Ulusal",Star TV
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.startv.com.tr/
#EXTVLCOPT:adaptive-max-bandwidth=3500000
#EXTVLCOPT:preferred-resolution=720
{base}/star

#EXTINF:-1 group-title="Haber",A Haber
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.ahaber.com.tr/
#EXTVLCOPT:adaptive-max-bandwidth=3500000
#EXTVLCOPT:preferred-resolution=720
{base}/ahaber

#EXTINF:-1 group-title="Ulusal",TRT 1
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
