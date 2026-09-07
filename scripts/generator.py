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

def is_free_server(s):
    name = s.get("Name", "").upper()
    tier = s.get("Tier", 0)
    if "FREE" in name or tier == 0:
        return True
    return False

def fetch_servers():
    url = "https://account.protonvpn.com/api/vpn/v2/logicals"
    try:
        res = requests.get(url, headers=HEADERS, timeout=20)
        if res.status_code == 200:
            servers = res.json().get("LogicalServers", [])
            active = [s for s in servers if s.get("Status") == 1]
            free = [s for s in active if is_free_server(s)]
            return free if free else active
    except Exception:
        pass

    fallback_url = "https://api.protonvpn.ch/vpn/logicals"
    try:
        res_fb = requests.get(fallback_url, headers={"x-pm-appversion": "Other"}, timeout=20)
        if res_fb.status_code == 200:
            servers_fb = res_fb.json().get("LogicalServers", [])
            active_fb = [s for s in servers_fb if s.get("Status") == 1]
            free_fb = [s for s in active_fb if is_free_server(s)]
            return free_fb if free_fb else active_fb
    except Exception:
        pass

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
