from flask import Flask, redirect, Response, request
import requests
import re

app = Flask(__name__)

# Genel Ayarlar
TIMEOUT = 15  # Bağlantı zaman aşımı süresi

def get_stream_from_source(url, referer, regex_pattern):
    """
    Belirtilen siteye gider, tarayıcı gibi davranır ve m3u8 linkini bulur.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": referer,
        "Origin": referer
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        
        # Regex ile linki avla
        match = re.search(regex_pattern, response.text)
        
        if match:
            found_url = match.group(1)
            # Link içindeki kaçış karakterlerini temizle (\/ -> /)
            found_url = found_url.replace('\\/', '/')
            return found_url
        else:
            return None
    except Exception as e:
        print(f"Hata ({url}): {e}")
        return None

# --- NOW TV ---
@app.route('/now')
def now():
    stream_url = get_stream_from_source(
        url="https://www.nowtv.com.tr/canli-yayin",
        referer="https://www.nowtv.com.tr/",
        regex_pattern=r"daionUrl\s*:\s*.*?'(https://.*?\.m3u8.*?)'"
    )
    if stream_url:
        return redirect(stream_url, code=302)
    return "NOW TV Linki Bulunamadi", 404

# --- ATV ---
@app.route('/atv')
def atv():
    # Önce siteden dinamik çekmeyi dener
    stream_url = get_stream_from_source(
        url="https://www.atv.com.tr/canli-yayin",
        referer="https://www.atv.com.tr/",
        regex_pattern=r"[\"'](https://.*?atv.*?\.m3u8.*?)[\"']"
    )
    # Bulamazsa statik yedeği kullanır
    if not stream_url:
        stream_url = "https://tmgrup.daioncdn.net/atv/atv.m3u8"
    return redirect(stream_url, code=302)

# --- SHOW TV ---
@app.route('/show')
def show():
    stream_url = get_stream_from_source(
        url="https://www.showtv.com.tr/canli-yayin",
        referer="https://www.showtv.com.tr/",
        regex_pattern=r"[\"'](https://.*?showtv.*?\.m3u8.*?)[\"']"
    )
    if stream_url:
        return redirect(stream_url, code=302)
    # Yedek (Ciner Live)
    return redirect("https://ciner-live.daioncdn.net/showtv/showtv.m3u8", code=302)

# --- A HABER ---
@app.route('/ahaber')
def ahaber():
    stream_url = get_stream_from_source(
        url="https://www.ahaber.com.tr/video/canli-yayin",
        referer="https://www.ahaber.com.tr/",
        regex_pattern=r"[\"'](https://.*?ahaber.*?\.m3u8.*?)[\"']"
    )
    if not stream_url:
        stream_url = "https://tmgrup.daioncdn.net/ahaber/ahaber.m3u8"
    return redirect(stream_url, code=302)

# --- TRT 1 (GÜNCELLENDİ: TABİİ.COM) ---
@app.route('/trt1')
def trt1():
    # İstediğiniz spesifik tabii linkini tarar
    target_url = "https://www.tabii.com/tr/watch/live/trt1?trackId=150002"
    
    stream_url = get_stream_from_source(
        url=target_url,
        referer="https://www.tabii.com/",
        # Tabii içinde genellikle 'master.m3u8' içeren bir JSON veya script bulunur
        regex_pattern=r"[\"'](https://.*?trt1.*?\.m3u8.*?)[\"']"
    )
    
    if stream_url:
        return redirect(stream_url, code=302)
    
    # Eğer Tabii yapısı regex ile yakalanamazsa, TRT'nin değişmeyen master linki devreye girer
    return redirect("https://tv-trt1.medya.trt.com.tr/master.m3u8", code=302)

# --- STAR TV (YENİ EKLENDİ) ---
@app.route('/star')
def star():
    stream_url = get_stream_from_source(
        url="https://www.startv.com.tr/canli-yayin",
        referer="https://www.startv.com.tr/",
        regex_pattern=r"[\"'](https://.*?startv.*?\.m3u8.*?)[\"']"
    )
    if stream_url:
        return redirect(stream_url, code=302)
        
    # Star TV Yedek Linki (Doğuş Live)
    return redirect("https://dogus-live.daioncdn.net/startv/startv.m3u8", code=302)

# --- M3U LİSTESİ ---
@app.route('/playlist.m3u')
def playlist():
    host = request.host_url.rstrip('/')
    if not host.startswith('https'):
        host = host.replace('http', 'https')
        
    m3u_content = f"""#EXTM3U
#EXTINF:-1 group-title="Ulusal" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/2/23/NOW_TV_2024_logo.png",NOW TV
{host}/now

#EXTINF:-1 group-title="Ulusal" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/ATV_logo_%28Turkey%29.svg/1200px-ATV_logo_%28Turkey%29.svg.png",ATV
{host}/atv

#EXTINF:-1 group-title="Ulusal" tvg-logo="https://upload.wikimedia.org/wikipedia/tr/6/6f/Show_TV_logo.png",Show TV
{host}/show

#EXTINF:-1 group-title="Ulusal" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Star_TV_logo.svg/1200px-Star_TV_logo.svg.png",Star TV
{host}/star

#EXTINF:-1 group-title="Haber" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/A_Haber_logo.png/640px-A_Haber_logo.png",A Haber
{host}/ahaber

#EXTINF:-1 group-title="Ulusal" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/TRT_1_logo_2022.svg/1200px-TRT_1_logo_2022.svg.png",TRT 1
{host}/trt1
"""
    return Response(m3u_content, mimetype='audio/x-mpegurl')

@app.route('/')
def home():
    return "IPTV Sunucusu Aktif. Linkiniz: /playlist.m3u"

# Vercel Handler
def handler(request, *args, **kwargs):
    return app(request, *args, **kwargs)
