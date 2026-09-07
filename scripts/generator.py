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

def extract_servers_from_response(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        if "LogicalServers" in data:
            return data["LogicalServers"]
        if "Servers" in data:
            return data["Servers"]
    return []

def fetch_servers():
    endpoints = [
        ("https://account.proton.me/api/vpn/v2/logicals", HEADERS),
        ("https://account.protonvpn.com/api/vpn/v2/logicals", HEADERS),
        ("https://api.protonvpn.ch/vpn/logicals", {"x-pm-appversion": "Other"}),
        ("https://api.protonmail.ch/vpn/logicals", {"x-pm-appversion": "Other"})
    ]

    for url, headers in endpoints:
        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code == 200:
                raw_servers = extract_servers_from_response(res.json())
                if raw_servers:
                    active = [s for s in raw_servers if s.get("Status", 1) == 1]
                    free = [
                        s for s in active 
                        if s.get("Tier") == 0 or "FREE" in str(s.get("Name", "")).upper()
                    ]
                    if free:
                        return free
                    if active:
                        return active
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
