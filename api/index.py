from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
import requests
import re
import json

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
        
        # --- KANAL LİNKLERİ ---
        
        # 1. NOW TV
        if path == '/now':
            redirect_url = self.get_stream("https://www.nowtv.com.tr/canli-yayin", "https://www.nowtv.com.tr/", r"daionUrl\s*:\s*.*?'(https://.*?\.m3u8.*?)'")
        
        # 2. SHOW TV
        elif path == '/show':
            redirect_url = self.get_stream("https://www.showtv.com.tr/canli-yayin", "https://www.showtv.com.tr/", r"[\"'](https?://.*?showtv.*?\.m3u8.*?)[\"']")
            if not redirect_url: redirect_url = "https://ciner-live.daioncdn.net/showtv/showtv.m3u8"

        # 3. STAR TV
        elif path == '/star':
            redirect_url = self.get_stream("https://www.startv.com.tr/canli-yayin", "https://www.startv.com.tr/", r"[\"'](https?://.*?startv.*?\.m3u8.*?)[\"']")
            if not redirect_url: redirect_url = "https://dogus-live.daioncdn.net/startv/startv.m3u8"

        # 4. ATV
        elif path == '/atv':
            redirect_url = self.get_stream_multi_regex("https://www.atv.com.tr/canli-yayin", "https://www.atv.com.tr/", [r'"VideoUrl"\s*:\s*"(https?://.*?\.m3u8.*?)"', r"[\"'](https?://.*?atv.*?\.m3u8.*?)[\"']"])
            if not redirect_url: redirect_url = "https://trkvz-live.daioncdn.net/atv/atv.m3u8"

        # 5. A HABER
        elif path == '/ahaber':
            redirect_url = self.get_stream_multi_regex("https://www.ahaber.com.tr/video/canli-yayin", "https://www.ahaber.com.tr/", [r'"VideoUrl"\s*:\s*"(https?://.*?\.m3u8.*?)"', r"[\"'](https?://.*?ahaber.*?\.m3u8.*?)[\"']"])
            if not redirect_url: redirect_url = "https://trkvz-live.daioncdn.net/ahaber/ahaber.m3u8"

        # 6. A SPOR
        elif path == '/aspor':
            redirect_url = self.get_stream_multi_regex("https://www.aspor.com.tr/webtv/canli-yayin", "https://www.aspor.com.tr/", [r'"VideoUrl"\s*:\s*"(https?://.*?\.m3u8.*?)"', r"[\"'](https?://.*?aspor.*?\.m3u8.*?)[\"']"])
            if not redirect_url: redirect_url = "https://trkvz-live.daioncdn.net/aspor/aspor.m3u8"

        # --- TRT AİLESİ (TABİİ ÖZEL AYRIŞTIRICI) ---
        # Artık rastgele link değil, isme göre link çekiyoruz.

        elif path == '/trt1':
            redirect_url = self.get_tabii_stream("TRT 1")
            if not redirect_url: redirect_url = "https://tv-trt1.medya.trt.com.tr/master.m3u8"

        elif path == '/trthaber':
            redirect_url = self.get_tabii_stream("TRT Haber")
            if not redirect_url: redirect_url = "https://tv-trthaber.medya.trt.com.tr/master.m3u8"

        elif path == '/trtspor':
            redirect_url = self.get_tabii_stream("TRT Spor")
            if not redirect_url: redirect_url = "https://tv-trtspor1.medya.trt.com.tr/master.m3u8"
        
        elif path == '/trtbelgesel':
            redirect_url = self.get_tabii_stream("TRT Belgesel")

        elif path == '/trtcocuk':
            redirect_url = self.get_tabii_stream("TRT Çocuk")

        elif path == '/trtmuzik':
            redirect_url = self.get_tabii_stream("TRT Müzik")
            
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
            self.wfile.write("<h1>TRT Ailesi Eklendi!</h1><p>Link: <a href='/playlist.m3u'>/playlist.m3u</a></p>".encode())
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
    
    # 1. Standart Regex
    def get_stream(self, url, referer, regex):
        return self.get_stream_multi_regex(url, referer, [regex])

    # 2. Çoklu Regex
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
                    return found.replace("http://", "https://")
        except:
            pass
        return None

    # 3. TABİİ ÖZEL AYRIŞTIRICI (İsimle Kanal Bulma)
    def get_tabii_stream(self, channel_target_name):
        try:
            url = "https://www.tabii.com/tr/watch/live/trt1?trackId=150002"
            req_headers = HEADERS.copy()
            req_headers['Referer'] = "https://www.tabii.com/"
            
            r = requests.get(url, headers=req_headers, timeout=TIMEOUT)
            content = r.text
            
            # Tabii sayfasında tüm kanallar büyük bir JSON listesi içindedir.
            # Regex ile bu listeyi buluyoruz.
            # Genellikle: "siblings":[{...},{...}] veya "tvChannels":[{...}] formatındadır.
            # Biz basitçe .m3u8 içeren ve hedef kanalın adının geçtiği bloğu arayacağız.
            
            # Pratik Çözüm: Sayfa içeriğini parçalara bölüp aradığımız kanalı bulalım.
            # Kanal adını (örn: "TRT 1") ve ".m3u8" uzantısını yakın mesafede arıyoruz.
            
            # JSON verisi "videoUrl" veya "url" içinde linki tutar.
            # Önce kanal adının geçtiği yeri bulalım
            parts = content.split(channel_target_name)
            
            # Kanal adından sonraki kısımda ilk gelen .m3u8 linkini al.
            if len(parts) > 1:
                # Kanal isminin geçtiği yerden sonraki kısmı al (parts[1])
                target_area = parts[1] 
                # Bu alandaki ilk m3u8 linkini regex ile avla
                match = re.search(r'["\'](https?://.*?\.m3u8.*?)["\']', target_area)
                if match:
                    found = match.group(1).replace('\\/', '/')
                    return found.replace("http://", "https://")

        except Exception as e:
            print(f"Tabii Hatasi: {e}")
            pass
        return None

    def send_playlist(self):
        host = self.headers.get('Host')
        protocol = "https" if "localhost" not in host else "http"
        base = f"{protocol}://{host}"
        
        # M3U Listesi
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

#EXTINF:-1 group-title="Ulusal",TRT 1
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.tabii.com/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/trt1

#EXTINF:-1 group-title="Haber",TRT Haber
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.tabii.com/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/trthaber

#EXTINF:-1 group-title="Spor",TRT Spor
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.tabii.com/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/trtspor

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

#EXTINF:-1 group-title="Muzik",TRT Muzik
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.tabii.com/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/trtmuzik

#EXTINF:-1 group-title="Spor",tabii Spor
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.tabii.com/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/tabiispor
"""
        self.send_response(200)
        self.send_header('Content-type', 'audio/x-mpegurl')
        self.end_headers()
        self.wfile.write(m3u.encode('utf-8'))
