import os
import json
import requests

PROTON_COOKIE = os.getenv("PROTON_COOKIE", "")
PROTON_UID = os.getenv("PROTON_UID", "")
PROTON_USER = os.getenv("PROTON_USER", "")
PROTON_PASS = os.getenv("PROTON_PASS", "")

HEADERS = {
    "accept": "application/vnd.protonmail.v1+json",
    "x-pm-appversion": "web-vpn-settings@5.0.357.0",
    "x-pm-uid": PROTON_UID,
    "Cookie": PROTON_COOKIE,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def fetch_all_servers():
    endpoints = [
        "https://account-api.protonvpn.com/api/vpn/v2/logicals",
        "https://account.proton.me/api/vpn/v2/logicals",
        "https://account.protonvpn.com/api/vpn/v2/logicals",
        "https://api.protonvpn.ch/vpn/logicals"
    ]

    for url in endpoints:
        try:
            res = requests.get(url, headers=HEADERS, timeout=25)
            if res.status_code == 200:
                raw = res.json()
                items = raw.get("LogicalServers", []) if isinstance(raw, dict) else raw
                if items and isinstance(items, list):
                    return [s for s in items if s.get("Status", 1) == 1]
        except Exception:
            continue
    return []

def main():
    servers = fetch_all_servers()
    
    js_content = f"""window.STATIC_SERVERS = {json.dumps(servers, ensure_ascii=False)};
window.SECRET_CONFIG = {{
  user: "{PROTON_USER}",
  pass: "{PROTON_PASS}",
  wgPrivate: "UKZg5sKBtmgXRYbp8lugpdRnBwYzKfuWqsjeH/aKrU0="
}};
"""
    with open("servers.js", "w", encoding="utf-8") as f:
        f.write(js_content)

if __name__ == "__main__":
    main()
