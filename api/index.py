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
        if path == '/now':
            redirect_url = self.get_stream("https://www.nowtv.com.tr/canli-yayin", "https://www.nowtv.com.tr/", r"daionUrl\s*:\s*.*?'(https://.*?\.m3u8.*?)'")
        elif path == '/show':
            redirect_url = self.get_stream("https://www.showtv.com.tr/canli-yayin", "https://www.showtv.com.tr/", r"[\"'](https?://.*?showtv.*?\.m3u8.*?)[\"']")
            if not redirect_url: redirect_url = "https://ciner-live.daioncdn.net/showtv/showtv.m3u8"
        elif path == '/star':
            redirect_url = self.get_stream("https://www.startv.com.tr/canli-yayin", "https://www.startv.com.tr/", r"[\"'](https?://.*?startv.*?\.m3u8.*?)[\"']")
            if not redirect_url: redirect_url = "https://dogus-live.daioncdn.net/startv/startv.m3u8"
        elif path == '/atv':
            redirect_url = self.get_stream_multi_regex("https://www.atv.com.tr/canli-yayin", "https://www.atv.com.tr/", [r'"VideoUrl"\s*:\s*"(https?://.*?\.m3u8.*?)"', r"[\"'](https?://.*?atv.*?\.m3u8.*?)[\"']"])
            if not redirect_url: redirect_url = "https://trkvz-live.daioncdn.net/atv/atv.m3u8"
        elif path == '/ahaber':
            redirect_url = self.get_stream_multi_regex("https://www.ahaber.com.tr/video/canli-yayin", "https://www.ahaber.com.tr/", [r'"VideoUrl"\s*:\s*"(https?://.*?\.m3u8.*?)"', r"[\"'](https?://.*?ahaber.*?\.m3u8.*?)[\"']"])
            if not redirect_url: redirect_url = "https://trkvz-live.daioncdn.net/ahaber/ahaber.m3u8"
        elif path == '/aspor':
            redirect_url = self.get_stream_multi_regex("https://www.aspor.com.tr/webtv/canli-yayin", "https://www.aspor.com.tr/", [r'"VideoUrl"\s*:\s*"(https?://.*?\.m3u8.*?)"', r"[\"'](https?://.*?aspor.*?\.m3u8.*?)[\"']"])
            if not redirect_url: redirect_url = "https://trkvz-live.daioncdn.net/aspor/aspor.m3u8"

        # --- TRT AİLESİ (ONARILDI) ---

        elif path == '/trt1':
            # ÖNCEKİ SAĞLAM YÖNTEM: Linkin içinde "trt1" yazısını arar. En garantisi budur.
            redirect_url = self.get_stream_multi_regex("https://www.tabii.com/tr/watch/live/trt1?trackId=150002", "https://www.tabii.com/", [r"[\"'](https?://.*?trt1.*?\.m3u8.*?)[\"']", r'"hls"\s*:\s*"(https?://.*?\.m3u8.*?)"'])
            if not redirect_url: redirect_url = "https://tv-trt1.medya.trt.com.tr/master.m3u8"

        elif path == '/trt2':
            # TRT 2 için de isme değil linke bakarız
            redirect_url = self.get_stream_multi_regex("https://www.tabii.com/tr/watch/live/trt1?trackId=150002", "https://www.tabii.com/", [r"[\"'](https?://.*?trt2.*?\.m3u8.*?)[\"']"])
            if not redirect_url: redirect_url = self.get_tabii_stream(["TRT 2"])
            if not redirect_url: redirect_url = "https://tv-trt2.medya.trt.com.tr/master.m3u8"

        elif path == '/trthaber':
            redirect_url = self.get_stream_multi_regex("https://www.tabii.com/tr/watch/live/trt1?trackId=150002", "https://www.tabii.com/", [r"[\"'](https?://.*?trthaber.*?\.m3u8.*?)[\"']"])
            if not redirect_url: redirect_url = "https://tv-trthaber.medya.trt.com.tr/master.m3u8"

        elif path == '/trtspor':
            redirect_url = self.get_stream_multi_regex("https://www.tabii.com/tr/watch/live/trt1?trackId=150002", "https://www.tabii.com/", [r"[\"'](https?://.*?trtspor1.*?\.m3u8.*?)[\"']"])
            if not redirect_url: redirect_url = "https://tv-trtspor1.medya.trt.com.tr/master.m3u8"
        
        elif path == '/trtsporyildiz':
            redirect_url = self.get_tabii_stream(["TRT Spor Yıldız", "TRT Spor 2"])
            if not redirect_url: redirect_url = "https://tv-trtspor2.medya.trt.com.tr/master.m3u8"

        elif path == '/trtcocuk':
            redirect_url = self.get_tabii_stream(["TRT Çocuk"])
            if not redirect_url: redirect_url = "https://tv-trtcocuk.medya.trt.com.tr/master.m3u8"
            
        elif path == '/trtdiyanetcocuk':
            redirect_url = self.get_tabii_stream(["TRT Diyanet Çocuk", "Diyanet Çocuk"])
            if not redirect_url: redirect_url = "https://tv-trtdiyanet.medya.trt.com.tr/master.m3u8"

        elif path == '/trtbelgesel':
            redirect_url = self.get_tabii_stream(["TRT Belgesel"])
            if not redirect_url: redirect_url = "https://tv-trtbelgesel.medya.trt.com.tr/master.m3u8"

        elif path == '/trtmuzik':
            redirect_url = self.get_tabii_stream(["TRT Müzik"])
            if not redirect_url: redirect_url = "https://tv-trtmuzik.medya.trt.com.tr/master.m3u8"
            
        elif path == '/trteba':
            # EBA için "Split" yöntemi en iyisidir. Satır atlamayı umursamaz.
            redirect_url = self.get_tabii_stream(["TRT EBA İlkokul", "TRT EBA Ortaokul", "TRT EBA Lise", "EBA"])
            if not redirect_url: redirect_url = "https://tv-trtebailkokul.medya.trt.com.tr/master.m3u8"

        elif path == '/tabiispor':
            redirect_url = self.get_tabii_stream(["tabii Spor"])

        # --- PLAYLIST ---
        elif path == '/playlist.m3u':
            self.send_playlist()
            return

        elif path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("<h1>TRT 1 ve EBA Onarildi!</h1><p>Link: <a href='/playlist.m3u'>/playlist.m3u</a></p>".encode())
            return
        
        else:
            self.send_error(404, "Kanal Bulunamadi")
            return

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
                match = re.search(regex, content, re.IGNORECASE)
                if match:
                    found = match.group(1).replace('\\/', '/')
                    if found.startswith("http://"): found = found.replace("http://", "https://")
                    return found
        except:
            pass
        return None

    def get_tabii_stream(self, channel_names_list):
        try:
            url = "https://www.tabii.com/tr/watch/live/trt1?trackId=150002"
            req_headers = HEADERS.copy()
            req_headers['Referer'] = "https://www.tabii.com/"
            
            r = requests.get(url, headers=req_headers, timeout=TIMEOUT)
            content = r.text
            
            # SPLIT YÖNTEMİ (ESKİ & SAĞLAM YÖNTEM):
            # Regex yerine sayfa metnini "Kanal Adı"ndan itibaren ikiye böleriz.
            # Böylece satır atlama derdi olmaz, kanal adından hemen sonraki linki alırız.
            
            for name in channel_names_list:
                # İsim sayfada var mı?
                if name in content:
                    # Varsa o isimden sonrasını al
                    parts = content.split(name)
                    if len(parts) > 1:
                        target_area = parts[1] # İsmin sağ tarafı
                        
                        # İlk 1000 karakterde m3u8 ara (çok uzağa gitmesin diye)
                        search_zone = target_area[:1000]
                        
                        match = re.search(r'["\'](https?://.*?\.m3u8.*?)["\']', search_zone)
                        if match:
                            found = match.group(1).replace('\\/', '/')
                            return found.replace("http://", "https://")
        except Exception as e:
            pass
        return None

    def send_playlist(self):
        host = self.headers.get('Host')
        protocol = "https" if "localhost" not in host else "http"
        base = f"{protocol}://{host}"
        
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
