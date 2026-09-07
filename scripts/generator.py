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

def is_free(server):
    name = str(server.get("Name", "")).upper()
    tier = server.get("Tier", 0)
    return "FREE" in name or tier == 0

def fetch_servers():
    endpoints = [
        "https://account-api.protonvpn.com/api/vpn/v2/logicals?WithIpV6=1",
        "https://account.proton.me/api/vpn/v2/logicals?WithIpV6=1",
        "https://account.protonvpn.com/api/vpn/v2/logicals?WithIpV6=1",
        "https://api.protonvpn.ch/vpn/logicals?WithIpV6=1"
    ]

    for url in endpoints:
        try:
            res = requests.get(url, headers=HEADERS, timeout=15)
            if res.status_code == 200:
                data = res.json()
                raw_list = data.get("LogicalServers", [])
                if raw_list:
                    free_list = [s for s in raw_list if s.get("Status") == 1 and is_free(s)]
                    return free_list if free_list else [s for s in raw_list if s.get("Status") == 1]
        except Exception:
            continue
    return []

def main():
    servers = fetch_servers()
    
    js_content = f"""window.STATIC_SERVERS = {json.dumps(servers, ensure_ascii=False)};
window.SECRET_CONFIG = {{
  user: "{PROTON_USER}",
  pass: "{PROTON_PASS}",
  wgPrivate: "cGFzc3dvcmRfZXhhbXBsZV9wcml2YXRlX2tleV8xMjM0NTY="
}};
"""
    with open("servers.js", "w", encoding="utf-8") as f:
        f.write(js_content)

if __name__ == "__main__":
    main()
