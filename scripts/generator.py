import os
import requests
import base64
import json

PROTON_USER = os.getenv("PROTON_USER", "")
PROTON_PASS = os.getenv("PROTON_PASS", "")

def fetch_servers():
    url = "https://api.protonvpn.ch/vpn/logicals"
    headers = {"x-pm-appversion": "Other"}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        data = res.json()
        return [s for s in data.get("LogicalServers", []) if s.get("Status") == 1 and s.get("Tier") == 0]
    return []

def main():
    servers = fetch_servers()
    payload = {
        "user": PROTON_USER,
        "pass": PROTON_PASS,
        "updated": True
    }
    os.makedirs("data", exist_ok=True)
    with open("data/config_meta.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)

if __name__ == "__main__":
    main()
