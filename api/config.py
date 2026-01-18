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
    # --- TRT / TABİİ CHANNELS ---
    "trt1": {
        "name": "TRT 1",
        "url": "https://www.tabii.com/tr/watch/live/trt1",
        "referer": "https://www.tabii.com/",
        "regex": r"\"url\"\s*:\s*\"(https://[^\"]+?\.m3u8[^\"]*?)\"",
        "fallback": "https://tv-trt1.medya.trt.com.tr/master.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/TRT_1_logo_2022.svg/1200px-TRT_1_logo_2022.svg.png",
        "group": "Ulusal"
    },
    "trt2": {
        "name": "TRT 2",
        "url": "https://www.tabii.com/tr/watch/live/trt2",
        "referer": "https://www.tabii.com/",
        "regex": r"\"url\"\s*:\s*\"(https://[^\"]+?\.m3u8[^\"]*?)\"",
        "fallback": "https://tv-trt2.medya.trt.com.tr/master.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/TRT_2_logo_2019.svg/1200px-TRT_2_logo_2019.svg.png",
        "group": "Ulusal"
    },
    "trtspor": {
        "name": "TRT SPOR",
        "url": "https://www.tabii.com/tr/watch/live/trtspor",
        "referer": "https://www.tabii.com/",
        "regex": r"\"url\"\s*:\s*\"(https://[^\"]+?\.m3u8[^\"]*?)\"",
        "fallback": "https://tv-trtspor1.medya.trt.com.tr/master.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/TRT_Spor_logo.svg/1200px-TRT_Spor_logo.svg.png",
        "group": "Spor"
    },
    "trtsporyildiz": {
        "name": "TRT SPOR YILDIZ",
        "url": "https://www.tabii.com/tr/watch/live/trtsporyildiz",
        "referer": "https://www.tabii.com/",
        "regex": r"\"url\"\s*:\s*\"(https://[^\"]+?\.m3u8[^\"]*?)\"",
        "fallback": "https://trt.daioncdn.net/trtspor-yildiz/master.m3u8?app=clean",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/TRT_Yildiz_logo.svg/1200px-TRT_Yildiz_logo.svg.png",
        "group": "Spor"
    },
    "trthaber": {
        "name": "TRT HABER",
        "url": "https://www.tabii.com/tr/watch/live/trthaber",
        "referer": "https://www.tabii.com/",
        "regex": r"\"url\"\s*:\s*\"(https://[^\"]+?\.m3u8[^\"]*?)\"",
        "fallback": "https://tv-trthaber.medya.trt.com.tr/master.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/TRT_Haber_logo_2022.svg/1200px-TRT_Haber_logo_2022.svg.png",
        "group": "Haber"
    },
    "trtcocuk": {
        "name": "TRT ÇOCUK",
        "url": "https://www.tabii.com/tr/watch/live/trtcocuk",
        "referer": "https://www.tabii.com/",
        "regex": r"\"url\"\s*:\s*\"(https://[^\"]+?\.m3u8[^\"]*?)\"",
        "fallback": "https://tv-trtcocuk.medya.trt.com.tr/master.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/tr/thumb/a/a9/TRT_%C3%87ocuk_2021_logo.png/1200px-TRT_%C3%87ocuk_2021_logo.png",
        "group": "Çocuk"
    },
    "trtworld": {
        "name": "TRT WORLD",
        "url": "https://www.tabii.com/tr/watch/live/trtworld",
        "referer": "https://www.tabii.com/",
        "regex": r"\"url\"\s*:\s*\"(https://[^\"]+?\.m3u8[^\"]*?)\"",
        "fallback": "https://tv-trtworld.medya.trt.com.tr/master.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/TRT_World_logo.svg/1200px-TRT_World_logo.svg.png",
        "group": "Haber"
    },
    "trtbelgesel": {
        "name": "TRT BELGESEL",
        "url": "https://www.tabii.com/tr/watch/live/trtbelgesel",
        "referer": "https://www.tabii.com/",
        "regex": r"\"url\"\s*:\s*\"(https://[^\"]+?\.m3u8[^\"]*?)\"",
        "fallback": "https://tv-trtbelgesel.medya.trt.com.tr/master.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/TRT_Belgesel_logo_2019.svg/1200px-TRT_Belgesel_logo_2019.svg.png",
        "group": "Ulusal"
    },
    "trtmuzik": {
        "name": "TRT MÜZİK",
        "url": "https://www.tabii.com/tr/watch/live/trtmuzik",
        "referer": "https://www.tabii.com/",
        "regex": r"\"url\"\s*:\s*\"(https://[^\"]+?\.m3u8[^\"]*?)\"",
        "fallback": "https://tv-trtmuzik.medya.trt.com.tr/master.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/TRT_M%C3%BCzik_logo_2019.svg/1200px-TRT_M%C3%BCzik_logo_2019.svg.png",
        "group": "Müzik"
    },
    "trtturk": {
        "name": "TRT TÜRK",
        "url": "https://www.tabii.com/tr/watch/live/trtturk",
        "referer": "https://www.tabii.com/",
        "regex": r"\"url\"\s*:\s*\"(https://[^\"]+?\.m3u8[^\"]*?)\"",
        "fallback": "https://tv-trtturk.medya.trt.com.tr/master.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/TRT_Turk_logo_2022.svg/1200px-TRT_Turk_logo_2022.svg.png",
        "group": "Ulusal"
    },
    "trtkurdi": {
        "name": "TRT KURDÎ",
        "url": "https://www.tabii.com/tr/watch/live/trtkurdi",
        "referer": "https://www.tabii.com/",
        "regex": r"\"url\"\s*:\s*\"(https://[^\"]+?\.m3u8[^\"]*?)\"",
        "fallback": "https://tv-trtkurdi.medya.trt.com.tr/master.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/TRT_Kurdi_logo_2021.svg/1200px-TRT_Kurdi_logo_2021.svg.png",
        "group": "Ulusal"
    },
    "trtarabi": {
        "name": "TRT ARABİ",
        "url": "https://www.tabii.com/tr/watch/live/trtarabi",
        "referer": "https://www.tabii.com/",
        "regex": r"\"url\"\s*:\s*\"(https://[^\"]+?\.m3u8[^\"]*?)\"",
        "fallback": "https://tv-trtarabi.medya.trt.com.tr/master.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/TRT_Al_Arabiya_logo_2019.svg/1200px-TRT_Al_Arabiya_logo_2019.svg.png",
        "group": "Ulusal"
    },
    "trtavaz": {
        "name": "TRT AVAZ",
        "url": "https://www.tabii.com/tr/watch/live/trtavaz",
        "referer": "https://www.tabii.com/",
        "regex": r"\"url\"\s*:\s*\"(https://[^\"]+?\.m3u8[^\"]*?)\"",
        "fallback": "https://tv-trtavaz.medya.trt.com.tr/master.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/TRT_Avaz_logo.svg/1200px-TRT_Avaz_logo.svg.png",
        "group": "Ulusal"
    },
    "trtgenc": {
        "name": "TRT GENÇ",
        "url": "https://www.tabii.com/tr/watch/live/trtgenc",
        "referer": "https://www.tabii.com/",
        "regex": r"\"url\"\s*:\s*\"(https://[^\"]+?\.m3u8[^\"]*?)\"",
        "fallback": "https://tv-trtgenc.medya.trt.com.tr/master.m3u8",
        "logo": "https://cms-tabii-public-image.tabii.com/int/w750/q80/60417_0-0-4319-2099.png",
        "group": "Ulusal"
    },
    "tabiispor": {
        "name": "tabii Spor (Clear)",
        "url": "https://www.tabii.com/tr/watch/live/tabiispor",
        "referer": "https://www.tabii.com/",
        "regex": r"\"url\"\s*:\s*\"(https://[^\"]+?\.m3u8[^\"]*?)\"",
        "fallback": "https://beert7sqimrk0bfdupfgn6qew.medya.trt.com.tr/master.m3u8",
        "logo": "https://cms-tabii-public-image.tabii.com/int/w750/q80/59075_0-0-4319-2099.png",
        "group": "Spor"
    },
    "tabiitv": {
        "name": "tabii TV",
        "url": "https://www.tabii.com/tr/watch/live/tabiitv",
        "referer": "https://www.tabii.com/",
        "regex": r"\"url\"\s*:\s*\"(https://[^\"]+?\.m3u8[^\"]*?)\"",
        "fallback": "https://ceokzokgtd.erbvr.com/tabiitv/tabiitv.m3u8",
        "logo": "https://cms-tabii-public-image.tabii.com/int/w750/q80/45155_0-0-1919-1080.jpeg",
        "group": "Ulusal"
    },
    "tabiispor1": {
        "name": "tabii Spor 1",
        "url": "https://www.tabii.com/tr/watch/live/tabiispor1",
        "referer": "https://www.tabii.com/",
        "regex": r"\"url\"\s*:\s*\"(https://[^\"]+?\.m3u8[^\"]*?)\"",
        "fallback": "https://iaqzu4szhtzeqd0edpsayinle.medya.trt.com.tr/master.m3u8",
        "logo": "https://cms-tabii-public-image.tabii.com/int/w750/q80/59073_0-0-4319-2099.png",
        "group": "Spor"
    },
    "tabiispor2": {
        "name": "tabii Spor 2",
        "url": "https://www.tabii.com/tr/watch/live/tabiispor2",
        "referer": "https://www.tabii.com/",
        "regex": r"\"url\"\s*:\s*\"(https://[^\"]+?\.m3u8[^\"]*?)\"",
        "fallback": "https://klublsslubcgyiz7zqt5bz8il.medya.trt.com.tr/master.m3u8",
        "logo": "https://cms-tabii-public-image.tabii.com/int/w750/q80/59077_0-0-4319-2099.png",
        "group": "Spor"
    },
    "tabiispor3": {
        "name": "tabii Spor 3",
        "url": "https://www.tabii.com/tr/watch/live/tabiispor3",
        "referer": "https://www.tabii.com/",
        "regex": r"\"url\"\s*:\s*\"(https://[^\"]+?\.m3u8[^\"]*?)\"",
        "fallback": "https://iaqzu4szhtzeqd0edpsayinle1.medya.trt.com.tr/master.m3u8",
        "logo": "https://cms-tabii-assets.tabii.com/thumbnails/43011_f9240409-f815-46f0-be4c-eb9910d659be_720.jpeg",
        "group": "Spor"
    },
    "tabiispor4": {
        "name": "tabii Spor 4",
        "url": "https://www.tabii.com/tr/watch/live/tabiispor4",
        "referer": "https://www.tabii.com/",
        "regex": r"\"url\"\s*:\s*\"(https://[^\"]+?\.m3u8[^\"]*?)\"",
        "fallback": "https://klublsslubcgyiz7zqt5bz8il1.medya.trt.com.tr/master.m3u8",
        "logo": "https://cms-tabii-assets.tabii.com/thumbnails/43014_cc4468f7-9270-496e-bc3e-a89c3143c680_720.jpeg",
        "group": "Spor"
    },
    "tabiispor5": {
        "name": "tabii Spor 5",
        "url": "https://www.tabii.com/tr/watch/live/tabiispor5",
        "referer": "https://www.tabii.com/",
        "regex": r"\"url\"\s*:\s*\"(https://[^\"]+?\.m3u8[^\"]*?)\"",
        "fallback": "https://iaqzu4szhtzeqd0edpsayinle2.medya.trt.com.tr/master.m3u8",
        "logo": "https://cms-tabii-assets.tabii.com/thumbnails/43017_ed4e8c15-460d-4950-ba5d-165c27636e2f_720.jpeg",
        "group": "Spor"
    },
    "tabiispor6": {
        "name": "tabii Spor 6",
        "url": "https://www.tabii.com/tr/watch/live/tabiispor6",
        "referer": "https://www.tabii.com/",
        "regex": r"\"url\"\s*:\s*\"(https://[^\"]+?\.m3u8[^\"]*?)\"",
        "fallback": "https://klublsslubcgyiz7zqt5bz8il2.medya.trt.com.tr/master.m3u8",
        "logo": "https://cms-tabii-assets.tabii.com/thumbnails/43020_0be2cc2a-6091-4e20-8025-0d3221db01f1_720.jpeg",
        "group": "Spor"
    },
    "tabii-cocuk": {
        "name": "tabii Çocuk (Premium)",
        "url": "https://www.tabii.com/tr/watch/live/tabii-cocuk",
        "referer": "https://www.tabii.com/",
        "regex": r"\"url\"\s*:\s*\"(https://[^\"]+?\.m3u8[^\"]*?)\"",
        "logo": "https://cms-tabii-public-image.tabii.com/int/w750/q80/51549_0-0-1919-1080.jpeg",
        "group": "Çocuk"
    }
}
