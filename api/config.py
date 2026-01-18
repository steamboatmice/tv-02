# Global Settings
TIMEOUT = 10
CACHE_DURATION = 1800  # 30 minutes in seconds

# Identity
USER_AGENT = "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"

# Channel Configurations
CHANNELS = {
    "now": {
        "name": "NOW TV",
        "url": "https://www.nowtv.com.tr/canli-yayin",
        "referer": "https://www.nowtv.com.tr/",
        "regex": r"daionUrl\s*:\s*.*?'(https://.*?\.m3u8.*?)'",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/2/23/NOW_TV_2024_logo.png",
        "group": "Ulusal"
    },
    "atv": {
        "name": "ATV",
        "url": "https://www.atv.com.tr/canli-yayin",
        "referer": "https://www.atv.com.tr/",
        "regex": r"[\"'](https://.*?atv.*?\.m3u8.*?)[\"']",
        "fallback": "https://tmgrup.daioncdn.net/atv/atv.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/ATV_logo_%28Turkey%29.svg/1200px-ATV_logo_%28Turkey%29.svg.png",
        "group": "Ulusal"
    },
    "show": {
        "name": "Show TV",
        "url": "https://www.showtv.com.tr/canli-yayin",
        "referer": "https://www.showtv.com.tr/",
        "regex": r"[\"'](https://.*?showtv.*?\.m3u8.*?)[\"']",
        "fallback": "https://ciner-live.daioncdn.net/showtv/showtv.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/tr/6/6f/Show_TV_logo.png",
        "group": "Ulusal"
    },
    "star": {
        "name": "Star TV",
        "url": "https://www.startv.com.tr/canli-yayin",
        "referer": "https://www.startv.com.tr/",
        "regex": r"[\"'](https://.*?startv.*?\.m3u8.*?)[\"']",
        "fallback": "https://dogus-live.daioncdn.net/startv/startv.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Star_TV_logo.svg/1200px-Star_TV_logo.svg.png",
        "group": "Ulusal"
    },
    "ahaber": {
        "name": "A Haber",
        "url": "https://www.ahaber.com.tr/video/canli-yayin",
        "referer": "https://www.ahaber.com.tr/",
        "regex": r"[\"'](https://.*?ahaber.*?\.m3u8.*?)[\"']",
        "fallback": "https://tmgrup.daioncdn.net/ahaber/ahaber.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/A_Haber_logo.png/640px-A_Haber_logo.png",
        "group": "Haber"
    },
    "trt1": {
        "name": "TRT 1",
        "url": "https://www.tabii.com/tr/watch/live/trt1?trackId=150002",
        "referer": "https://www.tabii.com/",
        "regex": r"[\"'](https://.*?trt1.*?\.m3u8.*?)[\"']",
        "fallback": "https://tv-trt1.medya.trt.com.tr/master.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/TRT_1_logo_2022.svg/1200px-TRT_1_logo_2022.svg.png",
        "group": "Ulusal"
    }
}
