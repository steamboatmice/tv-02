\# Project Context: Serverless IPTV Proxy



\## Project Definition

This project is a lightweight, serverless IPTV Proxy service designed to run on Vercel. Its primary goal is to scrape dynamic, token-protected live stream links (`.m3u8`) from major Turkish TV broadcasters (TRT, ATV, NOW, etc.) and serve them via a static endpoint to clients like VLC or IPTV Smarters.



\## Core Principles \& Constraints (Strict Rules)

1\.  \*\*Pure Python Only:\*\* Do NOT use frameworks like Flask, Django, or FastAPI. Use only Python's native `http.server.BaseHTTPRequestHandler` and the `requests` library. This is crucial to minimize Vercel "Cold Start" latency.

2\.  \*\*Mobile Spoofing:\*\* All outgoing HTTP requests must use the User-Agent of a mobile device (Samsung S21/Android 13) to bypass web-only restrictions and ads.

&nbsp;   \* \*UA String:\* `Mozilla/5.0 (Linux; Android 13; SM-G991B)...`

3\.  \*\*Bandwidth Locking:\*\* The generated M3U playlist must force a bitrate limit to prevent buffering.

&nbsp;   \* \*Required Tag:\* `#EXTVLCOPT:adaptive-max-bandwidth=2000000` (Caps quality at ~720p/2Mbps).

4\.  \*\*Hybrid Parsing Engine:\*\* The scraping logic must support two modes:

&nbsp;   \* \*Regex Mode:\* For standard sites (NOW, Show TV) using regex patterns.

&nbsp;   \* \*Split Mode:\* For complex sites (Tabii/TRT) where string splitting is more reliable than regex to avoid newline issues.



\## Goal

To provide a stable, "set-and-forget" IPTV playlist for personal use that auto-heals when source links change.

