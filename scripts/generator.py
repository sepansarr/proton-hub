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

def is_truly_free(s):
    name = str(s.get("Name", "")).upper()
    tier = s.get("Tier", 0)
    if "FREE" in name:
        return True
    if tier == 0:
        return True
    return False

def extract_real_load(s):
    if "Load" in s and s["Load"] is not None:
        return int(round(float(s["Load"])))
    if "Score" in s and s["Score"] is not None:
        return int(round(float(s["Score"])))
    if s.get("Servers") and isinstance(s["Servers"], list) and len(s["Servers"]) > 0:
        sub = s["Servers"][0]
        if "Load" in sub and sub["Load"] is not None:
            return int(round(float(sub["Load"])))
    return 75

def fetch_free_servers():
    endpoints = [
        "https://account-api.protonvpn.com/api/vpn/v2/logicals?WithIpV6=1",
        "https://account.proton.me/api/vpn/v2/logicals?WithIpV6=1",
        "https://account.protonvpn.com/api/vpn/v2/logicals?WithIpV6=1",
        "https://api.protonvpn.ch/vpn/logicals?WithIpV6=1"
    ]

    for url in endpoints:
        try:
            res = requests.get(url, headers=HEADERS, timeout=20)
            if res.status_code == 200:
                raw = res.json()
                items = raw.get("LogicalServers", []) if isinstance(raw, dict) else raw
                if items and isinstance(items, list):
                    filtered = [s for s in items if s.get("Status", 1) == 1 and is_truly_free(s)]
                    for s in filtered:
                        s["ActualLoad"] = extract_real_load(s)
                    if filtered:
                        return filtered
        except Exception:
            continue
    return []

def main():
    servers = fetch_free_servers()
    
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
