import os
import json
import base64
import requests
from cryptography.hazmat.primitives.asymmetric import x25519

PROTON_USER = os.getenv("PROTON_USER", "")
PROTON_PASS = os.getenv("PROTON_PASS", "")

def generate_wg_keys():
    priv = x25519.X25519PrivateKey.generate()
    pub = priv.public_key()
    priv_b64 = base64.b64encode(priv.private_bytes_raw()).decode('utf-8')
    pub_b64 = base64.b64encode(pub.public_bytes_raw()).decode('utf-8')
    return priv_b64, pub_b64

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
    wg_private, wg_public = generate_wg_keys()

    payload = {
        "wg_private": wg_private,
        "wg_public": wg_public,
        "user": PROTON_USER,
        "pass": PROTON_PASS,
        "servers": servers
    }

    os.makedirs("data", exist_ok=True)
    with open("data/servers.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)

if __name__ == "__main__":
    main()
