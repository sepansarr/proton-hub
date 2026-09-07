const I18N = {
  fa: {
    brandTitle: "پروتون هاب",
    tagCloud: "ژنراتور پیشرفته کانفیگ",
    themeLabel: "حالت نمایش",
    langLabel: "زبان سامانه",
    prefixLabel: "پیشوند نام کانفیگ",
    protoLabel: "پروتکل خروجی",
    protoWg: "وایرگارد (WireGuard)",
    protoUdp: "اوپن‌وی‌پی‌ان (UDP)",
    protoTcp: "اوپن‌وی‌پی‌ان (TCP)",
    mainTitle: "سرورهای رسمی پروتون",
    mainSub: "فهرست کانفیگ‌های فعال با محاسبه بار زنده شبکه",
    statusLoading: "در حال بارگیری داده‌ها...",
    statusReady: "سرور فعال",
    fullServers: "سرور تکمیل ظرفیت (100%)",
    searchPlaceholder: "جستجوی کشور یا نام سرور...",
    dlBtn: "دریافت فایل",
    applyBtn: "اعمال",
    errConn: "سروری یافت نشد",
    toastPrefix: "پیشوند نام کانفیگ‌ها با موفقیت اعمال شد",
    toastProto: "پروتکل خروجی تغییر یافت",
    toastReload: "فهرست سرورها به‌روزرسانی شد",
    footerOwn: 'طراحی و توسعه توسط <a href="https://github.com/sepansarr" target="_blank" rel="noopener noreferrer">سپنسار</a>',
    footerDisclaimer: "این پروژه مستقل بوده و هیچ‌گونه وابستگی تجاری به Proton AG ندارد."
  },
  en: {
    brandTitle: "Proton Hub",
    tagCloud: "Advanced Config Generator",
    themeLabel: "Appearance",
    langLabel: "Language",
    prefixLabel: "Config Prefix",
    protoLabel: "Export Protocol",
    protoWg: "WireGuard",
    protoUdp: "OpenVPN (UDP)",
    protoTcp: "OpenVPN (TCP)",
    mainTitle: "Proton Official Servers",
    mainSub: "Active server inventory with real-time network load",
    statusLoading: "Loading server inventory...",
    statusReady: "Active Servers",
    fullServers: "Full Capacity Servers (100%)",
    searchPlaceholder: "Search country or server name...",
    dlBtn: "Download",
    applyBtn: "Apply",
    errConn: "No servers found",
    toastPrefix: "Filename prefix applied",
    toastProto: "Protocol changed",
    toastReload: "Servers refreshed",
    footerOwn: 'Crafted with precision by <a href="https://github.com/sepansarr" target="_blank" rel="noopener noreferrer">sepansar</a>',
    footerDisclaimer: "This independent project is not affiliated with Proton AG."
  }
};

const COUNTRY_NAMES = {
  US: "United States", NL: "Netherlands", JP: "Japan", CA: "Canada", DE: "Germany",
  CH: "Switzerland", GB: "United Kingdom", FR: "France", SE: "Sweden", IS: "Iceland",
  AU: "Australia", BR: "Brazil", SG: "Singapore", MX: "Mexico", NO: "Norway",
  DK: "Denmark", IT: "Italy", ES: "Spain", PL: "Poland", AT: "Austria"
};

const OFFICIAL_CA = `-----BEGIN CERTIFICATE-----
MIIFnTCCA4WgAwIBAgIUCI574SM3Lyh47GyNl0WAOYrqb5QwDQYJKoZIhvcNAQEL
BQAwXjELMAkGA1UEBhMCQ0gxHzAdBgNVBAoMFlByb3RvbiBUZWNobm9sb2dpZXMg
QUcxEjAQBgNVBAsMCVByb3RvblZQTjEaMBgGA1UEAwwRUHJvdG9uVlBOIFJvb3Qg
Q0EwHhcNMTkxMDE3MDgwNjQxWhcNMzkxMDEyMDgwNjQxWjBeMQswCQYDVQQGEwJD
SDEfMB0GA1UECgwWUHJvdG9uIFRlY2hub2xvZ2llcyBBRzESMBAGA1UECwwJUHJv
dG9uVlBOMRowGAYDVQQDDBFQcm90b25WUE4gUm9vdCBDQTCCAiIwDQYJKoZIhvcN
AQEBBQADggIPADCCAgoCggIBAMkUT7zMUS5C+NjQ7YoGpVFlfbN9HFgG4JiKfHB8
QxnPPRgyTi0zVOAj1ImsRilauY8Ddm5dQtd8qcApoz6oCx5cFiiSQG2uyhS/59Zl
5wqIkw1o+CgwZgeWkq04lcrxhhfPgJZRFjrYVezy/Z2Ssd18s3/FFNQ+2iV1KC2K
z8eSPr50u+l9vEKsKiNGkJTdlWjoDKZM2C15i/h8Smi+PdJlx7WMTtYoVC1Fzq0r
aCPDQl18kspu11b6d8ECPWghKcDIIKuA0r0nGqF1GvH1AmbC/xUaNrKgz9AfioZL
MP/l22tVG3KKM1ku0eYHX7NzNHgkM2JKnBBannImQQBGTAcvvUlnfF3AHx4vzx7H
ahpBz8ebThx2uv+vzu8lCVEcKjQObGwLbAONJN2enug8hwSSZQv7tz7onDQWlYh0
El5fnkrEQGbukNnSyOqTwfobvBllIPzBqdO38eZFA0YTlH9plYjIjPjGl931lFAA
3G9t0x7nxAauLXN5QVp1yoF1tzXc5kN0SFAasM9VtVEOSMaGHLKhF+IMyVX8h5Iu
IRC8u5O672r7cHS+Dtx87LjxypqNhmbf1TWyLJSoh0qYhMr+BbO7+N6zKRIZPI5b
MXc8Be2pQwbSA4ZrDvSjFC9yDXmSuZTyVo6Bqi/KCUZeaXKof68oNxVYeGowNeQd
g/znAgMBAAGjUzBRMB0GA1UdDgQWBBR44WtTuEKCaPPUltYEHZoyhJo+4TAfBgNV
HSMEGDAWgBR44WtTuEKCaPPUltYEHZoyhJo+4TAPBgNVHRMBAf8EBTADAQH/MA0G
CSqGSIb3DQEBCwUAA4ICAQBBmzCQlHxOJ6izys3TVpaze+rUkA9GejgsB2DZXIcm
4Lj/SNzQsPlZRu4S0IZV253dbE1DoWlHanw5lnXwx8iU82X7jdm/5uZOwj2NqSqT
bTn0WLAC6khEKKe5bPTf18UOcwN82Le3AnkwcNAaBO5/TzFQVgnVedXr2g6rmpp9
gdedeEl9acB7xqfYfkrmijqYMm+xeG2rXaanch3HjweMDuZdT/Ub5G6oir0Kowft
lA1ytjXRg+X+yWymTpF/zGLYfSodWWjMKhpzZtRJZ+9B0pWXUyY7SuCj5T5SMIAu
x3NQQ46wSbHRolIlwh7zD7kBgkyLe7ByLvGFKa2Vw4PuWjqYwrRbFjb2+EKAwPu6
VTWz/QQTU8oJewGFipw94Bi61zuaPvF1qZCHgYhVojRy6KcqncX2Hx9hjfVxspBZ
DrVH6uofCmd99GmVu+qizybWQTrPaubfc/a2jJIbXc2bRQjYj/qmjE3hTlmO3k7V
EP6i8CLhEl+dX75aZw9StkqjdpIApYwX6XNDqVuGzfeTXXclk4N4aDPwPFM/Yo/e
KnvlNlKbljWdMYkfx8r37aOHpchH34cv0Jb5Im+1H07ywnshXNfUhRazOpubJRHn
bjDuBwWS1/Vwp5AJ+QHsPXhJdl3qHc1szJZVJb3VyAWvG/bWApKfFuZX18tiI4N0
EA==
-----END CERTIFICATE-----`;

const OFFICIAL_TLS_CRYPT = `-----BEGIN OpenVPN Static key V1-----
6acef03f62675b4b1bbd03e53b187727
423cea742242106cb2916a8a4c829756
3d22c7e5cef430b1103c6f66eb1fc5b3
75a672f158e2e2e936c3faa48b035a6d
e17beaac23b5f03b10b868d53d03521d
8ba115059da777a60cbfd7b2c9c57472
78a15b8f6e68a3ef7fd583ec9f398c8b
d4735dab40cbd1e3c62a822e97489186
c30a0b48c7c38ea32ceb056d3fa5a710
e10ccc7a0ddb363b08c3d2777a3395e1
0c0b6080f56309192ab5aacd4b45f55d
a61fc77af39bd81a19218a79762c3386
2df55785075f37d8c71dc8a42097ee43
344739a0dd48d03025b0450cf1fb5e8c
aeb893d9a96d1f15519bb3c4dcb40ee3
16672ea16c012664f8a9f11255518deb
-----END OpenVPN Static key V1-----`;

let currentLang = "fa";
let currentProtocol = "wireguard";
let activePrefix = "Sepansar";
let serverDataset = [];
let openGroups = {};

const themeCheckbox = document.getElementById("theme-ios-checkbox");
const btnFa = document.getElementById("btn-fa");
const btnEn = document.getElementById("btn-en");
const customPrefix = document.getElementById("custom-prefix");
const btnApplyPrefix = document.getElementById("btn-apply-prefix");
const txtApply = document.getElementById("txt-apply");
const searchBox = document.getElementById("search-box");
const statusCounter = document.getElementById("status-counter");
const fullCounterBadge = document.getElementById("full-counter-badge");
const fullCounterText = document.getElementById("full-counter-text");
const btnReload = document.getElementById("btn-reload");
const tableWrapper = document.querySelector(".table-wrapper");
const toast = document.getElementById("toast");

const txtBrandTitle = document.getElementById("txt-brand-title");
const tagCloud = document.getElementById("tag-cloud");
const txtThemeLabel = document.getElementById("txt-theme-label");
const txtLangLabel = document.getElementById("txt-lang-label");
const lblCustomPrefix = document.getElementById("lbl-custom-prefix");
const lblProtocol = document.getElementById("lbl-protocol");
const txtProtoWg = document.getElementById("txt-proto-wg");
const txtProtoUdp = document.getElementById("txt-proto-udp");
const txtProtoTcp = document.getElementById("txt-proto-tcp");
const txtMainTitle = document.getElementById("txt-main-title");
const txtMainSubtitle = document.getElementById("txt-main-subtitle");
const txtFooterOwn = document.getElementById("txt-footer-own");
const txtFooterDisclaimer = document.getElementById("txt-footer-disclaimer");

function showToast(msg) {
  toast.textContent = msg;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 2500);
}

function initTheme() {
  const saved = localStorage.getItem("sepansar_theme") || "dark";
  document.documentElement.setAttribute("data-theme", saved);
  themeCheckbox.checked = (saved === "light");
}

themeCheckbox.addEventListener("change", () => {
  const targetTheme = themeCheckbox.checked ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", targetTheme);
  localStorage.setItem("sepansar_theme", targetTheme);
});

function applyLanguage(lang) {
  currentLang = lang;
  document.documentElement.lang = lang;
  document.documentElement.dir = lang === "fa" ? "rtl" : "ltr";

  btnFa.classList.toggle("active", lang === "fa");
  btnEn.classList.toggle("active", lang === "en");

  const t = I18N[lang];
  txtBrandTitle.textContent = t.brandTitle;
  tagCloud.textContent = t.tagCloud;
  txtThemeLabel.textContent = t.themeLabel;
  txtLangLabel.textContent = t.langLabel;
  lblCustomPrefix.textContent = t.prefixLabel;
  lblProtocol.textContent = t.protoLabel;
  txtProtoWg.textContent = t.protoWg;
  txtProtoUdp.textContent = t.protoUdp;
  txtProtoTcp.textContent = t.protoTcp;
  txtMainTitle.textContent = t.mainTitle;
  txtMainSubtitle.textContent = t.mainSub;
  searchBox.placeholder = t.searchPlaceholder;
  txtApply.textContent = t.applyBtn;
  txtFooterOwn.innerHTML = t.footerOwn;
  txtFooterDisclaimer.textContent = t.footerDisclaimer;

  renderServerList();
}

btnFa.addEventListener("click", () => applyLanguage("fa"));
btnEn.addEventListener("click", () => applyLanguage("en"));

btnApplyPrefix.addEventListener("click", () => {
  activePrefix = customPrefix.value.trim() || "Sepansar";
  renderServerList();
  showToast(I18N[currentLang].toastPrefix);
});

document.querySelectorAll(".proto-card").forEach((card) => {
  card.addEventListener("click", () => {
    document.querySelectorAll(".proto-card").forEach((c) => c.classList.remove("active"));
    card.classList.add("active");
    currentProtocol = card.dataset.proto;
    renderServerList();
    showToast(`${I18N[currentLang].toastProto}: ${card.querySelector(".proto-title").textContent}`);
  });
});

btnReload.addEventListener("click", () => {
  btnReload.classList.add("spinning");
  const s = document.createElement("script");
  s.src = "servers.js?t=" + Date.now();
  s.onload = () => {
    btnReload.classList.remove("spinning");
    loadServers();
    showToast(I18N[currentLang].toastReload);
  };
  document.body.appendChild(s);
});

searchBox.addEventListener("input", renderServerList);

function loadServers() {
  if (window.STATIC_SERVERS && Array.isArray(window.STATIC_SERVERS) && window.STATIC_SERVERS.length > 0) {
    serverDataset = window.STATIC_SERVERS;
    renderServerList();
  } else {
    statusCounter.textContent = I18N[currentLang].errConn;
  }
}

function getCountryFlag(code) {
  if (!code || code.length !== 2) return "https://flagcdn.com/w40/un.png";
  return `https://flagcdn.com/w40/${code.toLowerCase()}.png`;
}

function renderServerList() {
  const t = I18N[currentLang];
  const query = searchBox.value.trim().toLowerCase();

  const filtered = serverDataset.filter((s) => {
    const name = (s.Name || "").toLowerCase();
    const country = (s.ExitCountry || "").toLowerCase();
    const cName = (COUNTRY_NAMES[s.ExitCountry] || "").toLowerCase();
    return name.includes(query) || country.includes(query) || cName.includes(query);
  });

  const fullCount = filtered.filter(s => (s.Load !== undefined ? Math.round(s.Load) : 0) >= 100).length;

  statusCounter.textContent = `${filtered.length} ${t.statusReady}`;
  
  if (fullCount > 0) {
    fullCounterBadge.style.display = "flex";
    fullCounterText.textContent = `${fullCount} ${t.fullServers}`;
  } else {
    fullCounterBadge.style.display = "none";
  }

  tableWrapper.innerHTML = "";

  const groups = {};
  filtered.forEach((srv) => {
    const cCode = srv.ExitCountry || "Other";
    if (!groups[cCode]) groups[cCode] = [];
    groups[cCode].push(srv);
  });

  Object.keys(groups).sort().forEach((countryCode) => {
    const list = groups[countryCode];
    const groupDiv = document.createElement("div");
    
    const isOpen = openGroups[countryCode] !== undefined ? openGroups[countryCode] : true;
    groupDiv.className = `country-group ${isOpen ? "open" : ""}`;

    const countryName = COUNTRY_NAMES[countryCode] || countryCode;

    const header = document.createElement("div");
    header.className = "country-header";
    header.innerHTML = `
      <div class="country-info">
        <img class="country-flag" src="${getCountryFlag(countryCode)}" alt="${countryCode}">
        <span>${countryName}</span>
      </div>
      <div class="country-header-actions">
        <span class="country-count">${list.length}</span>
        <svg class="arrow-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
      </div>
    `;

    header.addEventListener("click", () => {
      const nowOpen = groupDiv.classList.toggle("open");
      openGroups[countryCode] = nowOpen;
    });

    const bodyDiv = document.createElement("div");
    bodyDiv.className = "country-body";

    list.forEach((srv) => {
      const row = document.createElement("div");
      row.className = "server-row";

      const ext = currentProtocol === "wireguard" ? ".conf" : ".ovpn";
      const displayName = `${activePrefix}-${srv.Name}${ext}`;
      const load = srv.Load !== undefined ? Math.round(srv.Load) : 80;
      const color = load >= 100 ? "var(--danger)" : load > 85 ? "var(--warning)" : "var(--success)";

      const hasIpv6 = Boolean(srv.Features && (srv.Features & 16 || srv.Features & 32));

      row.innerHTML = `
        <span class="server-name">${displayName}</span>
        <div class="server-meta">
          <div class="status-indicator" style="color: ${color};">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <span>${load}%</span>
          </div>
          ${hasIpv6 ? '<span class="ipv6-badge">IPv6</span>' : ''}
          <button class="dl-btn">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            <span>${t.dlBtn}</span>
          </button>
        </div>
      `;

      row.querySelector(".dl-btn").addEventListener("click", () => exportConfig(srv));
      bodyDiv.appendChild(row);
    });

    groupDiv.appendChild(header);
    groupDiv.appendChild(bodyDiv);
    tableWrapper.appendChild(groupDiv);
  });
}

function exportConfig(srv) {
  const finalFilename = `${activePrefix}-${srv.Name}`;
  const ip = srv.Servers && srv.Servers[0] ? srv.Servers[0].EntryIP : srv.Domain;
  const cfg = window.SECRET_CONFIG || { user: "username", pass: "password", wgPrivate: "UKZg5sKBtmgXRYbp8lugpdRnBwYzKfuWqsjeH/aKrU0=" };

  if (currentProtocol === "wireguard") {
    const pubKey = srv.Servers && srv.Servers[0] ? srv.Servers[0].X25519PublicKey || "" : "";
    const payload = `[Interface]
# Bouncing = 1
# NAT-PMP (Port Forwarding) = off
# VPN Accelerator = on
PrivateKey = ${cfg.wgPrivate}
Address = 10.2.0.2/32, 2a07:b944::2:2/128
DNS = 10.2.0.1, 2a07:b944::2:1

[Peer]
# ${srv.Name}
PublicKey = ${pubKey}
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = ${ip}:51820
PersistentKeepalive = 25
`;
    executeBlobDownload(`${finalFilename}.conf`, payload);
  } else {
    const isTcp = currentProtocol === "openvpn-tcp";
    const proto = isTcp ? "tcp" : "udp";
    const ports = isTcp ? [443, 8443, 5060] : [80, 5060, 1194, 51820, 4569];
    const remoteDirectives = ports.map((p) => `remote ${ip} ${p}`).join("\n");

    const authSection = (cfg.user && cfg.pass)
      ? `<auth-user-pass>\n${cfg.user}\n${cfg.pass}\n</auth-user-pass>`
      : `auth-user-pass`;

    const payload = `# ==============================================================================
# Copyright (c) Proton AG (Switzerland)
# Generated via Proton Hub (sepansar)
# Server: ${srv.Name}
# ==============================================================================

client
dev tun
proto ${proto}

${remoteDirectives}

remote-random
resolv-retry infinite
nobind

cipher AES-256-GCM

setenv CLIENT_CERT 0
tun-mtu 1500
mssfix 0
persist-key
persist-tun

reneg-sec 0

remote-cert-tls server
${authSection}

<ca>
${OFFICIAL_CA}
</ca>

<tls-crypt>
${OFFICIAL_TLS_CRYPT}
</tls-crypt>
`;
    executeBlobDownload(`${finalFilename}.ovpn`, payload);
  }
}

function executeBlobDownload(filename, body) {
  const blob = new Blob([body], { type: "text/plain;charset=utf-8" });
  const anchor = document.createElement("a");
  anchor.href = URL.createObjectURL(blob);
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  document.body.removeChild(anchor);
  URL.revokeObjectURL(anchor.href);
}

initTheme();
loadServers();
