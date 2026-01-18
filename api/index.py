from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
import requests
import re

# --- AYARLAR ---
TIMEOUT = 12
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
        
        # --- ANA KANALLAR ---
        
        # NOW TV
        if path == '/now':
            redirect_url = self.get_stream("https://www.nowtv.com.tr/canli-yayin", "https://www.nowtv.com.tr/", r"daionUrl\s*:\s*.*?'(https://.*?\.m3u8.*?)'")
        
        # SHOW TV
        elif path == '/show':
            redirect_url = self.get_stream("https://www.showtv.com.tr/canli-yayin", "https://www.showtv.com.tr/", r"[\"'](https?://.*?showtv.*?\.m3u8.*?)[\"']")
            if not redirect_url: redirect_url = "https://ciner-live.daioncdn.net/showtv/showtv.m3u8"

        # STAR TV
        elif path == '/star':
            redirect_url = self.get_stream("https://www.startv.com.tr/canli-yayin", "https://www.startv.com.tr/", r"[\"'](https?://.*?startv.*?\.m3u8.*?)[\"']")
            if not redirect_url: redirect_url = "https://dogus-live.daioncdn.net/startv/startv.m3u8"

        # ATV
        elif path == '/atv':
            redirect_url = self.get_stream_multi_regex("https://www.atv.com.tr/canli-yayin", "https://www.atv.com.tr/", [r'"VideoUrl"\s*:\s*"(https?://.*?\.m3u8.*?)"', r"[\"'](https?://.*?atv.*?\.m3u8.*?)[\"']"])
            if not redirect_url: redirect_url = "https://trkvz-live.daioncdn.net/atv/atv.m3u8"

        # A HABER
        elif path == '/ahaber':
            redirect_url = self.get_stream_multi_regex("https://www.ahaber.com.tr/video/canli-yayin", "https://www.ahaber.com.tr/", [r'"VideoUrl"\s*:\s*"(https?://.*?\.m3u8.*?)"', r"[\"'](https?://.*?ahaber.*?\.m3u8.*?)[\"']"])
            if not redirect_url: redirect_url = "https://trkvz-live.daioncdn.net/ahaber/ahaber.m3u8"

        # A SPOR
        elif path == '/aspor':
            redirect_url = self.get_stream_multi_regex("https://www.aspor.com.tr/webtv/canli-yayin", "https://www.aspor.com.tr/", [r'"VideoUrl"\s*:\s*"(https?://.*?\.m3u8.*?)"', r"[\"'](https?://.*?aspor.*?\.m3u8.*?)[\"']"])
            if not redirect_url: redirect_url = "https://trkvz-live.daioncdn.net/aspor/aspor.m3u8"

        # --- TRT AİLESİ (TABİİ OTOMATİK TARAMA) ---

        elif path == '/trt1':
            redirect_url = self.get_tabii_stream("TRT 1")
            if not redirect_url: redirect_url = "https://tv-trt1.medya.trt.com.tr/master.m3u8"

        elif path == '/trt2':
            redirect_url = self.get_tabii_stream("TRT 2")
            if not redirect_url: redirect_url = "https://tv-trt2.medya.trt.com.tr/master.m3u8"

        elif path == '/trthaber':
            redirect_url = self.get_tabii_stream("TRT Haber")
            if not redirect_url: redirect_url = "https://tv-trthaber.medya.trt.com.tr/master.m3u8"

        elif path == '/trtspor':
            redirect_url = self.get_tabii_stream("TRT Spor")
            if not redirect_url: redirect_url = "https://tv-trtspor1.medya.trt.com.tr/master.m3u8"
        
        elif path == '/trtsporyildiz':
            # Hem "TRT Spor Yıldız" hem "TRT Spor 2" olarak arar
            redirect_url = self.get_tabii_stream("TRT Spor Yıldız")
            if not redirect_url: redirect_url = self.get_tabii_stream("TRT Spor 2")
            if not redirect_url: redirect_url = "https://tv-trtspor2.medya.trt.com.tr/master.m3u8"

        elif path == '/trtcocuk':
            redirect_url = self.get_tabii_stream("TRT Çocuk")
            if not redirect_url: redirect_url = "https://tv-trtcocuk.medya.trt.com.tr/master.m3u8"
            
        elif path == '/trtdiyanetcocuk':
            redirect_url = self.get_tabii_stream("TRT Diyanet Çocuk")
            # Yedek link tahmini
            if not redirect_url: redirect_url = "https://tv-trtdiyanet.medya.trt.com.tr/master.m3u8"

        elif path == '/trtbelgesel':
            redirect_url = self.get_tabii_stream("TRT Belgesel")
            if not redirect_url: redirect_url = "https://tv-trtbelgesel.medya.trt.com.tr/master.m3u8"

        elif path == '/trtmuzik':
            redirect_url = self.get_tabii_stream("TRT Müzik")
            if not redirect_url: redirect_url = "https://tv-trtmuzik.medya.trt.com.tr/master.m3u8"
            
        elif path == '/trteba':
            # EBA genellikle İlkokul/Ortaokul diye ayrılır. Bu "TRT EBA" adını arar, ilk bulduğunu getirir.
            redirect_url = self.get_tabii_stream("TRT EBA")
            if not redirect_url: redirect_url = "https://tv-trtebailkokul.medya.trt.com.tr/master.m3u8"

        elif path == '/tabiispor':
            redirect_url = self.get_tabii_stream("tabii Spor")


        # --- PLAYLIST ---
        elif path == '/playlist.m3u':
            self.send_playlist()
            return

        elif path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("<h1>Tum Kanallar (TRT Full + Turkuvaz) Aktif!</h1><p>Link: <a href='/playlist.m3u'>/playlist.m3u</a></p>".encode())
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
            self.send_error(404, "Link Bulunamadi")

    # --- YARDIMCI FONKSİYONLAR ---
    def get_stream(self, url, referer, regex):
        return self.get_stream_multi_regex(url, referer, [regex])

    def get_stream_multi_regex(self, url, referer, regex_list):
        try:
            req_headers = HEADERS.copy()
            req_headers['Referer'] = referer
            r = requests.get(url, headers=req_headers, timeout=TIMEOUT)
            content = r.text.replace('\u002F', '/') 
            for regex in regex_list:
                match = re.search(regex, content)
                if match:
                    found = match.group(1).replace('\\/', '/')
                    if found.startswith("http://"):
                        found = found.replace("http://", "https://")
                    return found
        except:
            pass
        return None

    def get_tabii_stream(self, channel_target_name):
        try:
            # TRT 1 sayfasındaki "Tüm Kanallar" verisini kullanıyoruz
            url = "https://www.tabii.com/tr/watch/live/trt1?trackId=150002"
            req_headers = HEADERS.copy()
            req_headers['Referer'] = "https://www.tabii.com/"
            
            r = requests.get(url, headers=req_headers, timeout=TIMEOUT)
            content = r.text
            
            # Basit Mantık: Kanal adını bul (örn: "TRT Spor Yıldız") -> Sonrasındaki ilk m3u8'i al.
            parts = content.split(channel_target_name)
            if len(parts) > 1:
                target_area = parts[1]
                # En yakın m3u8 linkini regex ile avla
                match = re.search(r'["\'](https?://.*?\.m3u8.*?)["\']', target_area)
                if match:
                    found = match.group(1).replace('\\/', '/')
                    return found.replace("http://", "https://")

        except:
            pass
        return None

    def send_playlist(self):
        host = self.headers.get('Host')
        protocol = "https" if "localhost" not in host else "http"
        base = f"{protocol}://{host}"
        
        # OYNATMA LISTESI (Guncel)
        m3u = f"""#EXTM3U
#EXTINF:-1 group-title="Ulusal",NOW TV
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.nowtv.com.tr/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/now

#EXTINF:-1 group-title="Ulusal",ATV
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.atv.com.tr/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/atv

#EXTINF:-1 group-title="Ulusal",Show TV
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.showtv.com.tr/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/show

#EXTINF:-1 group-title="Ulusal",Star TV
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.startv.com.tr/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/star

#EXTINF:-1 group-title="Ulusal",TRT 1
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.tabii.com/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/trt1

#EXTINF:-1 group-title="Ulusal",TRT 2
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.tabii.com/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/trt2

#EXTINF:-1 group-title="Haber",TRT Haber
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.tabii.com/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/trthaber

#EXTINF:-1 group-title="Haber",A Haber
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.ahaber.com.tr/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/ahaber

#EXTINF:-1 group-title="Spor",A Spor
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.aspor.com.tr/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/aspor

#EXTINF:-1 group-title="Spor",TRT Spor
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.tabii.com/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/trtspor

#EXTINF:-1 group-title="Spor",TRT Spor Yildiz
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.tabii.com/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/trtsporyildiz

#EXTINF:-1 group-title="Spor",tabii Spor
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.tabii.com/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/tabiispor

#EXTINF:-1 group-title="Belgesel",TRT Belgesel
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.tabii.com/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/trtbelgesel

#EXTINF:-1 group-title="Cocuk",TRT Cocuk
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.tabii.com/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/trtcocuk

#EXTINF:-1 group-title="Cocuk",TRT Diyanet Cocuk
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.tabii.com/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/trtdiyanetcocuk

#EXTINF:-1 group-title="Egitim",TRT EBA
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.tabii.com/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/trteba

#EXTINF:-1 group-title="Muzik",TRT Muzik
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.tabii.com/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/trtmuzik
"""
        self.send_response(200)
        self.send_header('Content-type', 'audio/x-mpegurl')
        self.end_headers()
        self.wfile.write(m3u.encode('utf-8'))
