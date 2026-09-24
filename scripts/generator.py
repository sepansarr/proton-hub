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
SUMMARY_PATH = os.getenv("GITHUB_STEP_SUMMARY", "")

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIGS_DIR = os.path.join(BASE_DIR, "data", "configs")

ENDPOINTS = [
    "https://account-api.protonvpn.com/api/vpn/v2/logicals?WithIpV6=1",
    "https://account.protonvpn.com/api/vpn/v2/logicals?WithIpV6=1",
    "https://account.proton.me/api/vpn/v2/logicals?WithIpV6=1",
    "https://api.protonvpn.ch/vpn/logicals?WithIpV6=1",
    "https://api.protonvpn.ch/vpn/logicals",
]

V1_ENDPOINTS = [
    "https://account-api.protonvpn.com/api/vpn/logicals",
    "https://account.protonvpn.com/api/vpn/logicals",
    "https://account.proton.me/api/vpn/logicals",
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
    for url in VERSION_SOURCES:
        try:
            res = requests.get(url, headers={"user-agent": USER_AGENT}, timeout=15)
            if res.status_code == 200:
                data = res.json()
                raw_version = data.get("version") if isinstance(data, dict) else None
                if raw_version:
                    candidate = normalize_version(str(raw_version))
                    if candidate not in versions:
                        versions.append(candidate)
        except Exception:
            continue
    return versions

def build_headers(version="web-vpn-settings@latest", authenticated=True):
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

def attempt_labels():
    labels = []
    if PROTON_COOKIE or PROTON_UID:
        labels.append(("auth", True))
    labels.append(("public", False))
    return labels

def is_truly_free(s):
    name = str(s.get("Name", "")).upper()
    tier = s.get("Tier", 0)
    return "FREE" in name or tier == 0

def parse_load(val):
    try:
        fval = float(val)
    except Exception:
        return None
    if fval < 0:
        return None
    if 0 < fval < 1:
        fval = fval * 100
    return max(0, min(100, int(round(fval))))

def fetch_from(url, headers, label):
    try:
        res = requests.get(url, headers=headers, timeout=25)
    except Exception:
        return [], False

    if res.status_code != 200:
        outdated = res.status_code == 422 and '"Code":5003' in res.text.replace(" ", "")
        return [], outdated

    try:
        raw = res.json()
    except ValueError:
        return [], False

    items = raw.get("LogicalServers", []) if isinstance(raw, dict) else raw
    if not isinstance(items, list):
        return [], False

    filtered = [s for s in items if s.get("Status", 1) == 1 and is_truly_free(s)]
    return filtered, False

def try_version(version):
    for label, authenticated in attempt_labels():
        headers = build_headers(version, authenticated)
        for url in ENDPOINTS:
            servers, outdated = fetch_from(url, headers, label)
            if servers:
                return servers
            if outdated:
                return []
    return []

def fetch_free_servers(versions):
    for version in versions:
        servers = try_version(version)
        if servers:
            return servers, version
    return [], ""

def fetch_v1_index(version):
    for label, authenticated in attempt_labels():
        headers = build_headers(version, authenticated)
        for url in V1_ENDPOINTS:
            try:
                res = requests.get(url, headers=headers, timeout=25)
                if res.status_code != 200:
                    continue
                raw = res.json()
                items = raw.get("LogicalServers", []) if isinstance(raw, dict) else raw
                if not isinstance(items, list):
                    continue

                by_id = {}
                by_name = {}
                with_load = 0
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    entry = {"Load": parse_load(item.get("Load")), "Status": item.get("Status")}
                    if entry["Load"] is not None:
                        with_load += 1
                    if item.get("ID"):
                        by_id[item["ID"]] = entry
                    if item.get("Name"):
                        by_name[item["Name"]] = entry

                if with_load > 0:
                    return by_id, by_name
            except Exception:
                continue
    return {}, {}

def apply_live_data(servers, by_id, by_name):
    result = []
    for s in servers:
        v1 = by_id.get(s.get("ID")) or by_name.get(s.get("Name"))
        load = parse_load(s.get("Load"))
        if load is None and v1 and v1["Load"] is not None:
            load = v1["Load"]
        if load is None:
            load = 80

        status = s.get("Status")
        if status is None and v1 and v1["Status"] is not None:
            status = v1["Status"]
        if status is not None and status != 1:
            continue

        s["ActualLoad"] = load
        result.append(s)
    return result

def download_official_configs(servers, version):
    os.makedirs(CONFIGS_DIR, exist_ok=True)
    headers = build_headers(version, True)

    for s in servers:
        s_name = s.get("Name")
        if not s_name:
            continue

        for proto in ["udp", "tcp"]:
            filename = f"{s_name}_{proto}.ovpn"
            filepath = os.path.join(CONFIGS_DIR, filename)
            url = f"https://account.protonvpn.com/api/vpn/v1/config/openvpn?Platform=Linux&Protocol={proto}&Server={s_name}"
            try:
                res = requests.get(url, headers=headers, timeout=10)
                if res.status_code == 200 and "client" in res.text:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(res.text)
                    s[f"config_ovpn_{proto}"] = f"data/configs/{filename}"
            except Exception:
                continue

def fetch_vpn_credentials(version):
    url = "https://account-api.protonvpn.com/api/core/v4/vpn"
    try:
        res = requests.get(url, headers=build_headers(version, True), timeout=15)
        if res.status_code == 200:
            data = res.json().get("VPN", {})
            user = data.get("Name")
            pwd = data.get("Password")
            if user and pwd:
                return user, pwd
    except Exception:
        pass
    return DEFAULT_USER, DEFAULT_PASS

def run():
    versions = discover_versions()
    if not versions:
        return 1

    servers, working_version = fetch_free_servers(versions)
    if not servers:
        return 1

    by_id, by_name = fetch_v1_index(working_version)
    servers = apply_live_data(servers, by_id, by_name)
    if not servers:
        return 1

    if PROTON_COOKIE or PROTON_UID:
        download_official_configs(servers, working_version)

    user, pwd = fetch_vpn_credentials(working_version)
    secret_config = {"user": user, "pass": pwd, "wgPrivate": WG_PRIVATE}

    js_content = (
        "window.STATIC_SERVERS = " + json.dumps(servers, ensure_ascii=False) + ";\n"
        "window.SECRET_CONFIG = " + json.dumps(secret_config, ensure_ascii=False, indent=2) + ";\n"
    )

    with open("servers.js", "w", encoding="utf-8") as f:
        f.write(js_content)

    return 0

def main():
    code = 1
    try:
        code = run()
    except Exception:
        log(traceback.format_exc())
    flush_report()
    sys.exit(code)

if __name__ == "__main__":
    main()
