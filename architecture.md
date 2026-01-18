\# Technical Architecture



\## File Structure

\- `/api/index.py`: The main entry point containing all backend logic (Handlers, Regex patterns, Playlist generation).

\- `/requirements.txt`: Dependencies file (Contains only `requests`).

\- `/vercel.json`: Routing configuration rewrites all traffic to `/api/index.py`.



\## Endpoint Logic

The application listens for GET requests on specific paths:

\- \*\*`/now`, `/show`, `/star`\*\*: Scrapes the respective website using Regex to find the `.m3u8` URL and returns a `302 Redirect`.

\- \*\*`/atv`, `/ahaber`, `/aspor`\*\*: Scrapes the "VideoUrl" variable from HTML using a multi-pattern Regex approach (handles both single and double quotes).

\- \*\*`/trt1`\*\*: Uses a Hybrid approach. First, it tries to fetch by channel name from the Tabii JSON structure. If that fails, it falls back to a direct Regex search for the specific stream link.

\- \*\*`/playlist.m3u`\*\*: Generates a dynamic M3U8 playlist file containing all supported channels with the `adaptive-max-bandwidth` optimization tags applied.



\## Key Functions

1\.  \*\*`get\_stream\_multi\_regex(url, referer, regex\_list)`\*\*: The core engine. It fetches the URL with the spoofed User-Agent and tries a list of regex patterns. It includes a fix for `re.IGNORECASE` to handle case-sensitivity issues.

2\.  \*\*`get\_tabii\_stream(channel\_names\_list)`\*\*: Specialized function for TRT/Tabii platform. It uses string splitting to locate the channel name in the source code and extracts the nearest `.m3u8` link, bypassing complex JSON parsing overhead.

3\.  \*\*`send\_playlist()`\*\*: Constructs the M3U file. It sorts the channel list alphabetically and applies VLC optimization tags.



\## Maintenance Guide

If a channel stops working:

1\.  Inspect the channel's live broadcast page source code.

2\.  Identify the new variable name holding the stream URL (e.g., changed from `VideoUrl` to `stream\_url`).

3\.  Update the Regex pattern in `api/index.py`.

