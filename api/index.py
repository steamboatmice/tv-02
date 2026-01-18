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
        
        # --- 1. YAYIN MOTORU ---
        
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

        # --- TRT AİLESİ ---

        elif path == '/trt1':
            # DÜZELTME: TRT 1 için "İsim Arama" (Tabii Stream) yerine "Direkt Link Arama" (Regex) kullanıyoruz.
            # Bu yöntem TRT 1'in kendi sayfasında şaşmaz.
            redirect_url = self.get_stream_multi_regex(
                "https://www.tabii.com/tr/watch/live/trt1?trackId=150002", 
                "https://www.tabii.com/", 
                [
                    r"[\"'](https?://.*?trt1.*?\.m3u8.*?)[\"']",  # İçinde trt1 geçen link
                    r'"hls"\s*:\s*"(https?://.*?\.m3u8.*?)"'      # JSON hls verisi
                ]
            )
            # Yedek
            if not redirect_url: redirect_url = "https://tv-trt1.medya.trt.com.tr/master.m3u8"

        elif path == '/trt2':
            # TRT 2 için de hibrit deniyoruz
            redirect_url = self.get_stream_multi_regex("https://www.tabii.com/tr/watch/live/trt1?trackId=150002", "https://www.tabii.com/", [r"[\"'](https?://.*?trt2.*?\.m3u8.*?)[\"']"])
            if not redirect_url: redirect_url = self.get_tabii_stream(["TRT 2"])
            if not redirect_url: redirect_url = "https://tv-trt2.medya.trt.com.tr/master.m3u8"

        elif path == '/trthaber':
            redirect_url = self.get_tabii_stream(["TRT Haber"])
            if not redirect_url: redirect_url = "https://tv-trthaber.medya.trt.com.tr/master.m3u8"

        elif path == '/trtspor':
            redirect_url = self.get_tabii_stream(["TRT Spor"])
            if not redirect_url: redirect_url = "https://tv-trtspor1.medya.trt.com.tr/master.m3u8"
        
        elif path == '/trtsporyildiz':
            redirect_url = self.get_tabii_stream(["TRT Spor Yıldız", "TRT Spor 2"])
            if not redirect_url: redirect_url = "https://tv-trtspor2.medya.trt.com.tr/master.m3u8"

        elif path == '/trtcocuk':
            redirect_url = self.get_tabii_stream(["TRT Çocuk"])
            if not redirect_url: redirect_url = "https://tv-trtcocuk.medya.trt.com.tr/master.m3u8"

        elif path == '/trtbelgesel':
            redirect_url = self.get_tabii_stream(["TRT Belgesel"])
            if not redirect_url: redirect_url = "https://tv-trtbelgesel.medya.trt.com.tr/master.m3u8"

        elif path == '/trtmuzik':
            redirect_url = self.get_tabii_stream(["TRT Müzik"])
            if not redirect_url: redirect_url = "https://tv-trtmuzik.medya.trt.com.tr/master.m3u8"

        elif path == '/tabiispor':
            redirect_url = self.get_tabii_stream(["tabii Spor"])

        # --- 2. LİSTE OLUŞTURUCU ---
        elif path == '/playlist.m3u':
            self.send_playlist()
            return

        elif path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("<h1>TRT 1 Onarildi!</h1><p>Link: <a href='/playlist.m3u'>/playlist.m3u</a></p>".encode())
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
                # TRT 1 için Case Insensitive (Büyük/Küçük harf duyarsız) çok önemli
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
            
            for name in channel_names_list:
                if name in content:
                    parts = content.split(name)
                    if len(parts) > 1:
                        target_area = parts[1]
                        match = re.search(r'["\'](https?://.*?\.m3u8.*?)["\']', target_area[:2000])
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
        
        # --- KANAL LİSTESİ ---
        channels = [
            ("NOW TV", "/now", "https://www.nowtv.com.tr/"),
            ("ATV", "/atv", "https://www.atv.com.tr/"),
            ("Show TV", "/show", "https://www.showtv.com.tr/"),
            ("Star TV", "/star", "https://www.startv.com.tr/"),
            ("A Haber", "/ahaber", "https://www.ahaber.com.tr/"),
            ("A Spor", "/aspor", "https://www.aspor.com.tr/"),
            ("TRT 1", "/trt1", "https://www.tabii.com/"),
            ("TRT 2", "/trt2", "https://www.tabii.com/"),
            ("TRT Haber", "/trthaber", "https://www.tabii.com/"),
            ("TRT Spor", "/trtspor", "https://www.tabii.com/"),
            ("TRT Spor Yıldız", "/trtsporyildiz", "https://www.tabii.com/"),
            ("TRT Belgesel", "/trtbelgesel", "https://www.tabii.com/"),
            ("TRT Çocuk", "/trtcocuk", "https://www.tabii.com/"),
            ("TRT Müzik", "/trtmuzik", "https://www.tabii.com/"),
            ("tabii Spor", "/tabiispor", "https://www.tabii.com/")
        ]

        # Alfabetik Siralama
        channels.sort(key=lambda x: x[0])

        m3u = "#EXTM3U\n"
        
        for name, path, ref in channels:
            m3u += f"#EXTINF:-1,{name}\n"
            m3u += f"#EXTVLCOPT:http-user-agent={UA_STRING}\n"
            m3u += f"#EXTVLCOPT:http-referrer={ref}\n"
            m3u += f"#EXTVLCOPT:adaptive-max-bandwidth=2000000\n"
            m3u += f"#EXTVLCOPT:preferred-resolution=720\n"
            m3u += f"{base}{path}\n\n"

        self.send_response(200)
        self.send_header('Content-type', 'audio/x-mpegurl')
        self.end_headers()
        self.wfile.write(m3u.encode('utf-8'))
