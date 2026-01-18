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
        
        # --- KANAL LİNKLERİ ---
        
        # 1. NOW TV (Sorunsuz)
        if path == '/now':
            redirect_url = self.get_stream("https://www.nowtv.com.tr/canli-yayin", "https://www.nowtv.com.tr/", r"daionUrl\s*:\s*.*?'(https://.*?\.m3u8.*?)'")
        
        # 2. SHOW TV (Sorunsuz)
        elif path == '/show':
            redirect_url = self.get_stream("https://www.showtv.com.tr/canli-yayin", "https://www.showtv.com.tr/", r"[\"'](https?://.*?showtv.*?\.m3u8.*?)[\"']")
            if not redirect_url: redirect_url = "https://ciner-live.daioncdn.net/showtv/showtv.m3u8"

        # 3. STAR TV (Sorunsuz)
        elif path == '/star':
            redirect_url = self.get_stream("https://www.startv.com.tr/canli-yayin", "https://www.startv.com.tr/", r"[\"'](https?://.*?startv.*?\.m3u8.*?)[\"']")
            if not redirect_url: redirect_url = "https://dogus-live.daioncdn.net/startv/startv.m3u8"

        # --- GÜNCELLENEN SORUNLU KANALLAR ---

        # 4. ATV (Turkuvaz HTML Analizi: "VideoUrl" içinde saklı)
        elif path == '/atv':
            # Önce MobileVideoUrl, sonra VideoUrl, en son standart m3u8 arar
            redirect_url = self.get_stream_multi_regex(
                "https://www.atv.com.tr/canli-yayin", 
                "https://www.atv.com.tr/", 
                [
                    r'"MobileVideoUrl"\s*:\s*"(https?://.*?\.m3u8.*?)"',
                    r'"VideoUrl"\s*:\s*"(https?://.*?\.m3u8.*?)"',
                    r"[\"'](https?://.*?atv.*?\.m3u8.*?)[\"']"
                ]
            )
            # Yedek: Backstage sunucusu
            if not redirect_url: redirect_url = "https://trkvz-live.daioncdn.net/atv/atv.m3u8"

        # 5. A HABER (Turkuvaz HTML Analizi)
        elif path == '/ahaber':
            redirect_url = self.get_stream_multi_regex(
                "https://www.ahaber.com.tr/video/canli-yayin", 
                "https://www.ahaber.com.tr/", 
                [
                    r'"MobileVideoUrl"\s*:\s*"(https?://.*?\.m3u8.*?)"',
                    r'"VideoUrl"\s*:\s*"(https?://.*?\.m3u8.*?)"',
                    r"[\"'](https?://.*?ahaber.*?\.m3u8.*?)[\"']"
                ]
            )
            if not redirect_url: redirect_url = "https://trkvz-live.daioncdn.net/ahaber/ahaber.m3u8"

        # 6. A SPOR (Yeni Eklendi - Turkuvaz HTML Analizi)
        elif path == '/aspor':
            redirect_url = self.get_stream_multi_regex(
                "https://www.aspor.com.tr/webtv/canli-yayin", 
                "https://www.aspor.com.tr/", 
                [
                    r'"MobileVideoUrl"\s*:\s*"(https?://.*?\.m3u8.*?)"',
                    r'"VideoUrl"\s*:\s*"(https?://.*?\.m3u8.*?)"',
                    r"[\"'](https?://.*?aspor.*?\.m3u8.*?)[\"']"
                ]
            )
            if not redirect_url: redirect_url = "https://trkvz-live.daioncdn.net/aspor/aspor.m3u8"

        # 7. TRT 1 (Tabii HTML Analizi: JSON içindeki 'hls' veya 'url' tagi)
        elif path == '/trt1':
            # Tabii.com yapısı çok dinamik, JSON içindeki "hls" anahtarını hedefliyoruz.
            redirect_url = self.get_stream_multi_regex(
                "https://www.tabii.com/tr/watch/live/trt1?trackId=150002", 
                "https://www.tabii.com/", 
                [
                    r'"hls"\s*:\s*"(https?://.*?\.m3u8.*?)"',
                    r'"url"\s*:\s*"(https?://.*?\.m3u8.*?)"',
                    r"[\"'](https?://.*?trt1.*?\.m3u8.*?)[\"']"
                ]
            )
            # Eğer Tabii HTML'den çıkmazsa, TRT İzle'nin eski ama sağlam API'sine bakarız
            if not redirect_url: redirect_url = "https://tv-trt1.medya.trt.com.tr/master.m3u8"

        # --- PLAYLIST ---
        elif path == '/playlist.m3u':
            self.send_playlist()
            return

        elif path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("<h1>Turkuvaz + TRT Yamasi Aktif!</h1><p>Link: <a href='/playlist.m3u'>/playlist.m3u</a></p>".encode())
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

    # --- TEKİL REGEX FONKSİYONU ---
    def get_stream(self, url, referer, regex):
        return self.get_stream_multi_regex(url, referer, [regex])

    # --- ÇOKLU REGEX FONKSİYONU (YENİ GÜÇLENDİRİLMİŞ TARAMA) ---
    def get_stream_multi_regex(self, url, referer, regex_list):
        try:
            req_headers = HEADERS.copy()
            req_headers['Referer'] = referer
            r = requests.get(url, headers=req_headers, timeout=TIMEOUT)
            
            # HTML içindeki JSON karakterlerini düzelt (Unicode kaçışları temizle)
            content = r.text.replace('\u002F', '/') 
            
            for regex in regex_list:
                match = re.search(regex, content)
                if match:
                    found_url = match.group(1).replace('\\/', '/')
                    # HTTP -> HTTPS Zorlaması (Güvenlik hatasını önler)
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
        
        # BITRATE: 2.0 Mbps (Stabilite Garantili)
        
        m3u = f"""#EXTM3U
#EXTINF:-1 group-title="Ulusal",NOW TV
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.nowtv.com.tr/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/now

#EXTINF:-1 group-title="Ulusal",ATV (Yeni)
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

#EXTINF:-1 group-title="Haber",A Haber (Yeni)
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.ahaber.com.tr/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/ahaber

#EXTINF:-1 group-title="Spor",A Spor (Yeni)
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.aspor.com.tr/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/aspor

#EXTINF:-1 group-title="Ulusal",TRT 1 (Tabii)
#EXTVLCOPT:http-user-agent={UA_STRING}
#EXTVLCOPT:http-referrer=https://www.tabii.com/
#EXTVLCOPT:adaptive-max-bandwidth=2000000
#EXTVLCOPT:preferred-resolution=720
{base}/trt1
"""
        self.send_response(200)
        self.send_header('Content-type', 'audio/x-mpegurl')
        self.end_headers()
        self.wfile.write(m3u.encode('utf-8'))
