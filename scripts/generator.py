import os
import sys
import json
import requests
import traceback

PROTON_COOKIE = os.getenv("PROTON_COOKIE", "").strip()
PROTON_UID = os.getenv("PROTON_UID", "").strip()
PROTON_APPVERSION = os.getenv("PROTON_APPVERSION", "").strip()
DEFAULT_USER = os.getenv("PROTON_USER", "")
DEFAULT_PASS = os.getenv("PROTON_PASS", "")
WG_PRIVATE = os.getenv("PROTON_WG_PRIVATE", "")

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
CONFIGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "configs")

def build_headers(version="web-vpn-settings@latest"):
    headers = {
        "accept": "application/vnd.protonmail.v1+json",
        "x-pm-appversion": version,
        "user-agent": USER_AGENT,
    }
    if PROTON_UID:
        headers["x-pm-uid"] = PROTON_UID
    if PROTON_COOKIE:
        headers["Cookie"] = PROTON_COOKIE
    return headers

def download_official_openvpn(server_name, platform="Linux", protocol="udp"):
    """
    دانلود فایل رسمی ovpn از اندپوینت اکانت پروتون
    """
    url = f"https://account.protonvpn.com/api/vpn/v1/config/openvpn?Platform={platform}&Protocol={protocol}&Server={server_name}"
    try:
        res = requests.get(url, headers=build_headers(), timeout=15)
        if res.status_code == 200 and "client" in res.text:
            return res.text
    except Exception as e:
        print(f"Error fetching OVPN for {server_name}: {e}")
    return None

def fetch_wg_devices():
    """
    دریافت کلیدهای فعال وایرگارد از API اکانت پروتون
    """
    url = "https://account-api.protonvpn.com/api/vpn/v1/wg-keys"
    try:
        res = requests.get(url, headers=build_headers(), timeout=15)
        if res.status_code == 200:
            return res.json().get("Keys", [])
    except Exception:
        pass
    return []
