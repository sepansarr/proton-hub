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

def fetch_servers():
    url = "https://account.protonvpn.com/api/vpn/v2/logicals"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        data = res.json()
        servers = data.get("LogicalServers", [])
        return [s for s in servers if s.get("Status") == 1 and s.get("Tier") == 0]
    
    fallback_url = "https://api.protonvpn.ch/vpn/logicals"
    res_fb = requests.get(fallback_url, headers={"x-pm-appversion": "Other"})
    if res_fb.status_code == 200:
        data_fb = res_fb.json()
        servers_fb = data_fb.get("LogicalServers", [])
        return [s for s in servers_fb if s.get("Status") == 1 and s.get("Tier") == 0]
    return []

def main():
    servers = fetch_servers()
    payload = {
        "user": PROTON_USER,
        "pass": PROTON_PASS,
        "servers": servers,
        "count": len(servers)
    }

    os.makedirs("data", exist_ok=True)
    with open("data/servers.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
