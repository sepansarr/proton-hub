import os
import sys
import json
import traceback
import requests

PROTON_COOKIE = os.getenv("PROTON_COOKIE", "")
PROTON_UID = os.getenv("PROTON_UID", "")
DEFAULT_USER = os.getenv("PROTON_USER", "")
DEFAULT_PASS = os.getenv("PROTON_PASS", "")
WG_PRIVATE = os.getenv("PROTON_WG_PRIVATE", "")
SUMMARY_PATH = os.getenv("GITHUB_STEP_SUMMARY", "")

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

ENDPOINTS = [
    "https://account-api.protonvpn.com/api/vpn/v2/logicals?WithIpV6=1",
    "https://account.protonvpn.com/api/vpn/v2/logicals?WithIpV6=1",
    "https://account.proton.me/api/vpn/v2/logicals?WithIpV6=1",
    "https://api.protonvpn.ch/vpn/logicals?WithIpV6=1",
    "https://api.protonvpn.ch/vpn/logicals",
]

REPORT = []


def log(message):
    REPORT.append(message)
    print(message, flush=True)


def flush_report():
    if not SUMMARY_PATH:
        return
    try:
        with open(SUMMARY_PATH, "a", encoding="utf-8") as f:
            f.write("### Generator report\n\n```\n")
            f.write("\n".join(REPORT))
            f.write("\n```\n")
    except Exception:
        pass


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
        log(f"[{label}] {url} -> request error: {type(e).__name__}: {e}")
        return []

    if res.status_code != 200:
        log(f"[{label}] {url} -> HTTP {res.status_code} body={res.text[:300]!r}")
        return []

    try:
        raw = res.json()
    except ValueError:
        log(f"[{label}] {url} -> HTTP 200 but body is not JSON: {res.text[:300]!r}")
        return []

    if isinstance(raw, dict):
        log(f"[{label}] {url} -> HTTP 200 keys={list(raw.keys())[:10]}")
        items = raw.get("LogicalServers", [])
    else:
        items = raw

    if not isinstance(items, list):
        log(f"[{label}] {url} -> HTTP 200 but no server list found")
        return []

    filtered = [s for s in items if s.get("Status", 1) == 1 and is_truly_free(s)]
    log(f"[{label}] {url} -> HTTP 200 total={len(items)} free_online={len(filtered)}")

    for s in filtered:
        s["ActualLoad"] = extract_real_load(s)
    return filtered


def fetch_free_servers():
    attempts = []
    if PROTON_COOKIE or PROTON_UID:
        attempts.append(("auth", auth_headers()))
    attempts.append(("public", public_headers()))

    log(f"attempt plan: {[a[0] for a in attempts]}")

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
                log("[credentials] fetched from Proton API")
                return user, pwd
            log("[credentials] HTTP 200 but Name/Password missing, using secrets fallback")
        else:
            log(f"[credentials] HTTP {res.status_code}, using secrets fallback")
    except Exception as e:
        log(f"[credentials] request error: {type(e).__name__}: {e}, using secrets fallback")
    return DEFAULT_USER, DEFAULT_PASS


def run():
    log("generator started")
    log(f"python={sys.version.split()[0]} requests={requests.__version__}")
    log(f"secrets present: cookie={bool(PROTON_COOKIE)} uid={bool(PROTON_UID)} user={bool(DEFAULT_USER)} pass={bool(DEFAULT_PASS)} wg={bool(WG_PRIVATE)}")

    servers = fetch_free_servers()
    if not servers:
        log("ERROR: no free servers could be fetched. servers.js was NOT modified.")
        return 1

    user, pwd = fetch_vpn_credentials()
    if not user or not pwd:
        log("ERROR: OpenVPN credentials are empty. servers.js was NOT modified.")
        return 1

    if not WG_PRIVATE:
        log("WARNING: PROTON_WG_PRIVATE secret is empty, WireGuard configs will be incomplete.")

    secret_config = {"user": user, "pass": pwd, "wgPrivate": WG_PRIVATE}

    js_content = (
        "window.STATIC_SERVERS = " + json.dumps(servers, ensure_ascii=False) + ";\n"
        "window.SECRET_CONFIG = " + json.dumps(secret_config, ensure_ascii=False, indent=2) + ";\n"
    )

    with open("servers.js", "w", encoding="utf-8") as f:
        f.write(js_content)

    log(f"servers.js written with {len(servers)} servers")
    return 0


def main():
    code = 1
    try:
        code = run()
    except Exception:
        log("UNEXPECTED EXCEPTION:")
        log(traceback.format_exc())
    flush_report()
    sys.exit(code)


if __name__ == "__main__":
    main()
