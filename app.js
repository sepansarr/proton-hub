const I18N = {
  fa: {
    brandTitle: "پروتون هاب",
    tagCloud: "تولیدکننده کانفیگ",
    themeLabel: "حالت نمایش",
    themeDark: "حالت تیره",
    themeLight: "حالت روشن",
    langLabel: "زبان سامانه",
    prefixLabel: "پیشوند نام فایل کانفیگ",
    protoLabel: "نوع پروتکل ارتباطی",
    protoWg: "وایرگارد",
    protoUdp: "اوپن‌وی‌پی‌ان (UDP)",
    protoTcp: "اوپن‌وی‌پی‌ان (TCP)",
    mainTitle: "سرورهای پروتون هاب",
    mainSub: "انتخاب سرور بر اساس کمترین میزان مصرف و موقعیت جغرافیایی",
    statusLoading: "در حال دریافت سرورها...",
    statusReady: "سرور فعال آماده دریافت",
    searchPlaceholder: "جستجوی کشور یا نام سرور...",
    dlBtn: "دانلود فایل",
    errConn: "سروری یافت نشد",
    footerOwn: 'طراحی و توسعه توسط <a href="https://github.com/sepansarr" target="_blank" rel="noopener noreferrer">سپنسار</a>',
    footerDisclaimer: "این پروژه مستقل بوده و هیچ‌گونه وابستگی تجاری به Proton AG ندارد."
  },
  en: {
    brandTitle: "Proton Hub",
    tagCloud: "Config Generator",
    themeLabel: "Appearance",
    themeDark: "Dark Mode",
    themeLight: "Light Mode",
    langLabel: "Language",
    prefixLabel: "Config File Prefix",
    protoLabel: "Protocol Type",
    protoWg: "WireGuard",
    protoUdp: "OpenVPN (UDP)",
    protoTcp: "OpenVPN (TCP)",
    mainTitle: "Proton Hub Servers",
    mainSub: "Select a server according to current load and position",
    statusLoading: "Fetching servers...",
    statusReady: "Active servers ready",
    searchPlaceholder: "Search country or server name...",
    dlBtn: "Download",
    errConn: "No servers found",
    footerOwn: 'Crafted with precision by <a href="https://github.com/sepansarr" target="_blank" rel="noopener noreferrer">sepansar</a>',
    footerDisclaimer: "This independent project is not affiliated with Proton AG."
  }
};

let currentLang = "fa";
let currentProtocol = "wireguard";
let serverDataset = [];

const btnFa = document.getElementById("btn-fa");
const btnEn = document.getElementById("btn-en");
const themeToggle = document.getElementById("theme-toggle");
const themeStatusText = document.getElementById("theme-status-text");
const txtThemeLabel = document.getElementById("txt-theme-label");
const txtBrandTitle = document.getElementById("txt-brand-title");
const tagCloud = document.getElementById("tag-cloud");
const customPrefix = document.getElementById("custom-prefix");
const searchBox = document.getElementById("search-box");
const statusCounter = document.getElementById("status-counter");
const tableWrapper = document.querySelector(".table-wrapper");

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

function initTheme() {
  const savedTheme = localStorage.getItem("sepansar_theme") || "dark";
  document.documentElement.setAttribute("data-theme", savedTheme);
  updateThemeText();
}

function updateThemeText() {
  const isLight = document.documentElement.getAttribute("data-theme") === "light";
  themeStatusText.textContent = isLight ? I18N[currentLang].themeLight : I18N[currentLang].themeDark;
}

themeToggle.addEventListener("click", () => {
  const current = document.documentElement.getAttribute("data-theme");
  const next = current === "light" ? "dark" : "light";
  document.documentElement.setAttribute("data-theme", next);
  localStorage.setItem("sepansar_theme", next);
  updateThemeText();
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
  txtFooterOwn.innerHTML = t.footerOwn;
  txtFooterDisclaimer.textContent = t.footerDisclaimer;

  updateThemeText();
  renderServerList();
}

btnFa.addEventListener("click", () => applyLanguage("fa"));
btnEn.addEventListener("click", () => applyLanguage("en"));

document.querySelectorAll(".proto-card").forEach((card) => {
  card.addEventListener("click", () => {
    document.querySelectorAll(".proto-card").forEach((c) => c.classList.remove("active"));
    card.classList.add("active");
    currentProtocol = card.dataset.proto;
  });
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
    const city = (s.City || "").toLowerCase();
    return name.includes(query) || country.includes(query) || city.includes(query);
  });

  statusCounter.textContent = `${filtered.length} ${t.statusReady}`;
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
    groupDiv.className = "country-group";

    const header = document.createElement("div");
    header.className = "country-header";
    header.innerHTML = `
      <div class="country-info">
        <img class="country-flag" src="${getCountryFlag(countryCode)}" alt="${countryCode}">
        <span>${list[0].City ? `${countryCode} - ${list[0].City}` : countryCode}</span>
      </div>
      <span class="country-count">${list.length}</span>
    `;

    const bodyDiv = document.createElement("div");
    bodyDiv.className = "country-body";

    list.forEach((srv) => {
      const row = document.createElement("div");
      row.className = "server-row";

      const prefix = customPrefix.value.trim() || "ProtonHub";
      const load = srv.Load !== undefined ? Math.round(srv.Load) : 75;
      const color = load > 85 ? "var(--danger)" : "var(--success)";

      row.innerHTML = `
        <span class="server-name">${prefix}-${srv.Name || "Server"}</span>
        <div class="server-meta">
          <div class="status-indicator" style="color: ${color};">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <span>${load}%</span>
          </div>
          <span class="ipv6-badge">IPv6</span>
          <button class="dl-btn">${t.dlBtn}</button>
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
  const prefix = customPrefix.value.trim() || "ProtonHub";
  const finalFilename = `${prefix}-${srv.Name || "VPN"}`;
  const ip = srv.Servers && srv.Servers[0] ? srv.Servers[0].EntryIP : srv.Domain;
  const cfg = window.SECRET_CONFIG || { user: "", pass: "", wgPrivate: "cGFzc3dvcmRfZXhhbXBsZV9wcml2YXRlX2tleV8xMjM0NTY=" };

  if (currentProtocol === "wireguard") {
    const pubKey = srv.Servers && srv.Servers[0] ? srv.Servers[0].X25519PublicKey || "" : "";
    const payload = `[Interface]
PrivateKey = ${cfg.wgPrivate}
Address = 10.2.0.2/32
DNS = 10.2.0.1

[Peer]
PublicKey = ${pubKey}
Endpoint = ${ip}:51820
AllowedIPs = 0.0.0.0/0
`;
    executeBlobDownload(`${finalFilename}.conf`, payload);
  } else {
    const isTcp = currentProtocol === "openvpn-tcp";
    const proto = isTcp ? "tcp" : "udp";
    const port = isTcp ? "443" : "1194";

    const authSection = (cfg.user && cfg.pass)
      ? `<auth-user-pass>\n${cfg.user}\n${cfg.pass}\n</auth-user-pass>`
      : `auth-user-pass`;

    const payload = `client
dev tun
proto ${proto}
remote ${ip} ${port}
resolv-retry infinite
nobind
persist-key
persist-tun
cipher AES-256-GCM
auth SHA512
verb 3
${authSection}
<ca>
-----BEGIN CERTIFICATE-----
MIIB/DCCAYWgAwIBAgIUQ1aG3K7...
-----END CERTIFICATE-----
</ca>
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
