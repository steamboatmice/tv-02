from flask import Flask, redirect, Response, request
import requests
import re

app = Flask(__name__)

# --- AYARLAR ---
TIMEOUT = 10
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.google.com/"
}

def get_stream(url, referer, regex):
    try:
        r = requests.get(url, headers={"User-Agent": HEADERS["User-Agent"], "Referer": referer}, timeout=TIMEOUT)
        match = re.search(regex, r.text)
        if match:
            return match.group(1).replace('\\/', '/')
    except:
        pass
    return None

# --- KANALLAR ---

@app.route('/now')
def now():
    link = get_stream("https://www.nowtv.com.tr/canli-yayin", "https://www.nowtv.com.tr/", r"daionUrl\s*:\s*.*?'(https://.*?\.m3u8.*?)'")
    return redirect(link, 302) if link else ("Link Yok", 404)

@app.route('/atv')
def atv():
    link = get_stream("https://www.atv.com.tr/canli-yayin", "https://www.atv.com.tr/", r"[\"'](https://.*?atv.*?\.m3u8.*?)[\"']")
    return redirect(link if link else "https://tmgrup.daioncdn.net/atv/atv.m3u8", 302)

@app.route('/show')
def show():
    link = get_stream("https://www.showtv.com.tr/canli-yayin", "https://www.showtv.com.tr/", r"[\"'](https://.*?showtv.*?\.m3u8.*?)[\"']")
    return redirect(link if link else "https://ciner-live.daioncdn.net/showtv/showtv.m3u8", 302)

@app.route('/ahaber')
def ahaber():
    link = get_stream("https://www.ahaber.com.tr/video/canli-yayin", "https://www.ahaber.com.tr/", r"[\"'](https://.*?ahaber.*?\.m3u8.*?)[\"']")
    return redirect(link if link else "https://tmgrup.daioncdn.net/ahaber/ahaber.m3u8", 302)

@app.route('/trt1')
def trt1():
    link = get_stream("https://www.tabii.com/tr/watch/live/trt1?trackId=150002", "https://www.tabii.com/", r"[\"'](https://.*?trt1.*?\.m3u8.*?)[\"']")
    return redirect(link if link else "https://tv-trt1.medya.trt.com.tr/master.m3u8", 302)

@app.route('/star')
def star():
    link = get_stream("https://www.startv.com.tr/canli-yayin", "https://www.startv.com.tr/", r"[\"'](https://.*?startv.*?\.m3u8.*?)[\"']")
    return redirect(link if link else "https://dogus-live.daioncdn.net/startv/startv.m3u8", 302)

# --- PLAYLIST ---
@app.route('/playlist.m3u')
def playlist():
    # HTTPS düzeltmesi
    base = request.host_url.rstrip('/').replace('http:', 'https:')
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
    return Response(m3u, mimetype='text/plain')

@app.route('/')
def home():
    return "Sunucu Aktif! Link: /playlist.m3u"

# --- VERCEL İÇİN KRİTİK NOKTA ---
# Bu fonksiyon Vercel'e "Benim uygulamam budur" der.
# Bunu eklediğimizde 'issubclass' hatası kaybolur.
def handler(request, *args, **kwargs):
    return app(request, *args, **kwargs)
