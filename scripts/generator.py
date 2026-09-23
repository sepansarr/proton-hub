import os
import sys
import json
import requests

PROTON_COOKIE = os.getenv("PROTON_COOKIE", "")
PROTON_UID = os.getenv("PROTON_UID", "")
DEFAULT_USER = os.getenv("PROTON_USER", "")
DEFAULT_PASS = os.getenv("PROTON_PASS", "")
WG_PRIVATE = os.getenv("PROTON_WG_PRIVATE", "")

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

ENDPOINTS = [
    "https://account-api.protonvpn.com/api/vpn/v2/logicals?WithIpV6=1",
    "https://account.protonvpn.com/api/vpn/v2/logicals?WithIpV6=1",
    "https://account.proton.me/api/vpn/v2/logicals?WithIpV6=1",
    "https://api.protonvpn.ch/vpn/logicals?WithIpV6=1",
    "https://api.protonvpn.ch/vpn/logicals",
]


def public_headers():
    return {
        "accept": "application/vnd.protonmail.v1+json",
        "x-pm-appversion": "web-vpn-settings@5.0.357.0",
        "user-agent": USER_AGENT,
    }


def auth_headers():
    headers = public_headers()
    if PROTON_UID:
        headers["x-pm-uid"] = PROTON_UID
    if PROTON_COOKIE:
        headers["Cookie"] = PROTON_COOKIE
    return headers


def is_truly_free(s):
    name = str(s.get("Name", "")).upper()
    tier = s.get("Tier", 0)
    if "FREE" in name:
        return True
    if tier == 0:
        return True
    return False


def to_percent(val):
    try:
        fval = float(val)
    except Exception:
        return None
    if fval < 0:
        return None
    if 0 < fval < 1 and not float(fval).is_integer():
        fval = fval * 100
    if fval > 100 and fval <= 1000:
        fval = fval / 10
    return max(0, min(100, int(round(fval))))


def extract_real_load(s):
    val = to_percent(s.get("Load"))
    if val is not None:
        return val

    servers = s.get("Servers")
    if isinstance(servers, list) and len(servers) > 0 and isinstance(servers[0], dict):
        val = to_percent(servers[0].get("Load"))
        if val is not None:
            return val

    return 80


def fetch_from(url, headers, label):
    try:
        res = requests.get(url, headers=headers, timeout=25)
    except Exception as e:
        print(f"[{label}] {url} -> request error: {type(e).__name__}", file=sys.stderr)
        return []

    if res.status_code != 200:
        print(f"[{label}] {url} -> HTTP {res.status_code}: {res.text[:200]!r}", file=sys.stderr)
        return []

    try:
        raw = res.json()
    except ValueError:
        print(f"[{label}] {url} -> HTTP 200 but response is not valid JSON", file=sys.stderr)
        return []

    items = raw.get("LogicalServers", []) if isinstance(raw, dict) else raw
    if not isinstance(items, list):
        print(f"[{label}] {url} -> HTTP 200 but no server list found", file=sys.stderr)
        return []

    filtered = [s for s in items if s.get("Status", 1) == 1 and is_truly_free(s)]
    print(f"[{label}] {url} -> HTTP 200, total={len(items)}, free_online={len(filtered)}")

    for s in filtered:
        s["ActualLoad"] = extract_real_load(s)
    return filtered


def fetch_free_servers():
    attempts = []
    if PROTON_COOKIE or PROTON_UID:
        attempts.append(("auth", auth_headers()))
    attempts.append(("public", public_headers()))

    for label, headers in attempts:
        for url in ENDPOINTS:
            result = fetch_from(url, headers, label)
            if result:
                return result
    return []


def fetch_vpn_credentials():
    url = "https://account-api.protonvpn.com/api/core/v4/vpn"
    try:
        res = requests.get(url, headers=auth_headers(), timeout=15)
        if res.status_code == 200:
            data = res.json().get("VPN", {})
            user = data.get("Name")
            pwd = data.get("Password")
            if user and pwd:
                print("[credentials] fetched from Proton API")
                return user, pwd
            print("[credentials] HTTP 200 but Name/Password missing", file=sys.stderr)
        else:
            print(f"[credentials] HTTP {res.status_code}, using secrets fallback", file=sys.stderr)
    except Exception as e:
        print(f"[credentials] request error: {type(e).__name__}, using secrets fallback", file=sys.stderr)
    return DEFAULT_USER, DEFAULT_PASS


def main():
    servers = fetch_free_servers()
    if not servers:
        print("ERROR: no free servers could be fetched. servers.js was NOT modified.", file=sys.stderr)
        sys.exit(1)

    user, pwd = fetch_vpn_credentials()
    if not user or not pwd:
        print("ERROR: OpenVPN credentials are empty. servers.js was NOT modified.", file=sys.stderr)
        sys.exit(1)

    if not WG_PRIVATE:
        print("WARNING: PROTON_WG_PRIVATE secret is empty, WireGuard configs will be incomplete.", file=sys.stderr)

    secret_config = {"user": user, "pass": pwd, "wgPrivate": WG_PRIVATE}

    js_content = (
        "window.STATIC_SERVERS = " + json.dumps(servers, ensure_ascii=False) + ";\n"
        "window.SECRET_CONFIG = " + json.dumps(secret_config, ensure_ascii=False, indent=2) + ";\n"
    )

    with open("servers.js", "w", encoding="utf-8") as f:
        f.write(js_content)

    print(f"servers.js written with {len(servers)} servers")


if __name__ == "__main__":
    main()
