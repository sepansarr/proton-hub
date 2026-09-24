import os
import sys
import json
import traceback
import requests

PROTON_COOKIE = os.getenv("PROTON_COOKIE", "").strip()
PROTON_UID = os.getenv("PROTON_UID", "").strip()
PROTON_APPVERSION = os.getenv("PROTON_APPVERSION", "").strip()
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

VERSION_SOURCES = [
    "https://account.protonvpn.com/assets/version.json",
    "https://account.proton.me/assets/version.json",
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


def normalize_version(value):
    value = value.strip()
    if not value:
        return ""
    if "@" in value:
        return value
    return "web-vpn-settings@" + value


def discover_versions():
    versions = []

    if PROTON_APPVERSION:
        versions.append(normalize_version(PROTON_APPVERSION))
        log(f"[version] using PROTON_APPVERSION secret: {versions[0]}")
    else:
        log("[version] PROTON_APPVERSION secret is empty")

    for url in VERSION_SOURCES:
        try:
            res = requests.get(url, headers={"user-agent": USER_AGENT}, timeout=15)
        except Exception as e:
            log(f"[version] {url} -> request error: {type(e).__name__}: {e}")
            continue

        if res.status_code != 200:
            log(f"[version] {url} -> HTTP {res.status_code}")
            continue

        try:
            data = res.json()
        except ValueError:
            log(f"[version] {url} -> HTTP 200 but body is not JSON: {res.text[:200]!r}")
            continue

        raw_version = data.get("version") if isinstance(data, dict) else None
        if not raw_version:
            log(f"[version] {url} -> HTTP 200 but no version field, keys={list(data.keys())[:10] if isinstance(data, dict) else type(data).__name__}")
            continue

        candidate = normalize_version(str(raw_version))
        log(f"[version] {url} -> discovered {candidate}")
        if candidate not in versions:
            versions.append(candidate)

    return versions


def build_headers(version, authenticated):
    headers = {
        "accept": "application/vnd.protonmail.v1+json",
        "x-pm-appversion": version,
        "user-agent": USER_AGENT,
    }
    if authenticated:
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
        return [], False

    if res.status_code != 200:
        outdated = res.status_code == 422 and '"Code":5003' in res.text.replace(" ", "")
        log(f"[{label}] {url} -> HTTP {res.status_code} body={res.text[:300]!r}")
        return [], outdated

    try:
        raw = res.json()
    except ValueError:
        log(f"[{label}] {url} -> HTTP 200 but body is not JSON: {res.text[:300]!r}")
        return [], False

    if isinstance(raw, dict):
        log(f"[{label}] {url} -> HTTP 200 keys={list(raw.keys())[:10]}")
        items = raw.get("LogicalServers", [])
    else:
        items = raw

    if not isinstance(items, list):
        log(f"[{label}] {url} -> HTTP 200 but no server list found")
        return [], False

    filtered = [s for s in items if s.get("Status", 1) == 1 and is_truly_free(s)]
    log(f"[{label}] {url} -> HTTP 200 total={len(items)} free_online={len(filtered)}")

    for s in filtered:
        s["ActualLoad"] = extract_real_load(s)
    return filtered, False


def try_version(version):
    labels = []
    if PROTON_COOKIE or PROTON_UID:
        labels.append(("auth", True))
    labels.append(("public", False))

    for label, authenticated in labels:
        headers = build_headers(version, authenticated)
        for url in ENDPOINTS:
            servers, outdated = fetch_from(url, headers, label)
            if servers:
                return servers
            if outdated:
                log(f"version rejected as out of date: {version}")
                return []
    return []


def fetch_free_servers(versions):
    for version in versions:
        log(f"trying app version: {version}")
        servers = try_version(version)
        if servers:
            return servers, version
    return [], ""


def fetch_vpn_credentials(version):
    url = "https://account-api.protonvpn.com/api/core/v4/vpn"
    try:
        res = requests.get(url, headers=build_headers(version, True), timeout=15)
        if res.status_code == 200:
            data = res.json().get("VPN", {})
            user = data.get("Name")
            pwd = data.get("Password")
            if user and pwd:
                log("[credentials] fetched from Proton API")
                return user, pwd
            log("[credentials] HTTP 200 but Name/Password missing, using secrets fallback")
        else:
            log(f"[credentials] HTTP {res.status_code} body={res.text[:200]!r}, using secrets fallback")
    except Exception as e:
        log(f"[credentials] request error: {type(e).__name__}: {e}, using secrets fallback")
    return DEFAULT_USER, DEFAULT_PASS


def run():
    log("generator started")
    log(f"python={sys.version.split()[0]} requests={requests.__version__}")
    log(f"secrets present: cookie={bool(PROTON_COOKIE)} uid={bool(PROTON_UID)} appversion={bool(PROTON_APPVERSION)} user={bool(DEFAULT_USER)} pass={bool(DEFAULT_PASS)} wg={bool(WG_PRIVATE)}")

    versions = discover_versions()
    if not versions:
        log("ERROR: no app version available. Set the PROTON_APPVERSION secret from the x-pm-appversion request header in your browser. servers.js was NOT modified.")
        return 1

    servers, working_version = fetch_free_servers(versions)
    if not servers:
        log("ERROR: no free servers could be fetched. servers.js was NOT modified.")
        return 1

    log(f"working app version: {working_version}")

    user, pwd = fetch_vpn_credentials(working_version)
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
