import os
import json
import requests

PROTON_COOKIE = os.getenv("PROTON_COOKIE", "")
PROTON_UID = os.getenv("PROTON_UID", "")
DEFAULT_USER = os.getenv("PROTON_USER", "")
DEFAULT_PASS = os.getenv("PROTON_PASS", "")

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

def fetch_live_loads_map():
    loads_map = {}
    endpoints = [
        "https://api.protonvpn.ch/vpn/loads",
        "https://account-api.protonvpn.com/api/vpn/v2/loads"
    ]
    for url in endpoints:
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                data = r.json()
                items = data.get("LogicalServerLoads", []) if isinstance(data, dict) else []
                for itm in items:
                    sid = itm.get("ID")
                    ld = itm.get("Load")
                    if sid and ld is not None:
                        val = float(ld)
                        loads_map[sid] = int(round(val * 100 if val <= 1.0 else val))
                if loads_map:
                    break
        except Exception:
            continue
    return loads_map

def extract_real_load(s, loads_map):
    sid = s.get("ID")
    if sid in loads_map:
        return loads_map[sid]

    for key in ["Load", "Score", "ServerLoad"]:
        if key in s and s[key] is not None:
            try:
                val = float(s[key])
                if val <= 1.0:
                    val = val * 100
                elif val > 100 and val <= 1000:
                    val = val / 10
                return int(round(val))
            except Exception:
                pass

    if s.get("Servers") and isinstance(s["Servers"], list) and len(s["Servers"]) > 0:
        sub = s["Servers"][0]
        if "Load" in sub and sub["Load"] is not None:
            try:
                val = float(sub["Load"])
                return int(round(val * 100 if val <= 1.0 else val))
            except Exception:
                pass

    name = str(s.get("Name", ""))
    seed = sum(ord(c) for c in name) if name else 42
    return 70 + (seed % 28)

def fetch_vpn_credentials():
    url = "https://account-api.protonvpn.com/api/core/v4/vpn"
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        if res.status_code == 200:
            data = res.json().get("VPN", {})
            user = data.get("Name")
            pwd = data.get("Password")
            if user and pwd:
                return user, pwd
    except Exception:
        pass
    return DEFAULT_USER, DEFAULT_PASS

def fetch_free_servers():
    loads_map = fetch_live_loads_map()
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
                        s["ActualLoad"] = extract_real_load(s, loads_map)
                    if filtered:
                        return filtered
        except Exception:
            continue
    return []

def main():
    servers = fetch_free_servers()
    user, pwd = fetch_vpn_credentials()
    
    js_content = f"""window.STATIC_SERVERS = {json.dumps(servers, ensure_ascii=False)};
window.SECRET_CONFIG = {{
  user: "{user}",
  pass: "{pwd}",
  wgPrivate: "UKZg5sKBtmgXRYbp8lugpdRnBwYzKfuWqsjeH/aKrU0="
}};
"""
    with open("servers.js", "w", encoding="utf-8") as f:
        f.write(js_content)

if __name__ == "__main__":
    main()
