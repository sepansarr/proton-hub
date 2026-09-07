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
    mainTitle: "سرورهای رایگان پروتون هاب",
    mainSub: "فهرست سرورهای فعال و بهینه‌سازی‌شده برای بارگیری مستقیم",
    statusLoading: "در حال دریافت سرورها...",
    statusReady: "سرور رایگان آماده بارگیری",
    searchPlaceholder: "جستجوی نام کشور، شهر یا آی‌پی...",
    thCountry: "کشور / شهر",
    thServer: "نام سرور",
    thLoad: "میزان مصرف سرور",
    thAction: "بارگیری",
    dlBtn: "دریافت فایل",
    errConn: "خطا در برقراری ارتباط با سرورها",
    footerOwn: 'طراحی و توسعه توسط <a href="https://github.com/sepansarr" target="_blank" rel="noopener noreferrer">سپنسار</a>',
    footerDisclaimer: "این پروژه مستقل بوده و هیچ‌گونه وابستگی تجاری به Proton AG ندارد. علامت تجاری Proton VPN متعلق به شرکت Proton AG است."
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
    mainTitle: "Proton Hub Free Servers",
    mainSub: "Active and optimized servers ready for direct download",
    statusLoading: "Fetching servers...",
    statusReady: "Free servers ready",
    searchPlaceholder: "Search country, city, or IP...",
    thCountry: "Location",
    thServer: "Server Name",
    thLoad: "Server Load",
    thAction: "Action",
    dlBtn: "Download",
    errConn: "Failed to connect to servers",
    footerOwn: 'Crafted with precision by <a href="https://github.com/sepansarr" target="_blank" rel="noopener noreferrer">sepansar</a>',
    footerDisclaimer: "This is an independent project and not affiliated with or endorsed by Proton AG. Proton VPN is a registered trademark of Proton AG."
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
const serversTbody = document.getElementById("servers-tbody");

const txtLangLabel = document.getElementById("txt-lang-label");
const lblCustomPrefix = document.getElementById("lbl-custom-prefix");
const lblProtocol = document.getElementById("lbl-protocol");
const txtProtoWg = document.getElementById("txt-proto-wg");
const txtProtoUdp = document.getElementById("txt-proto-udp");
const txtProtoTcp = document.getElementById("txt-proto-tcp");
const txtMainTitle = document.getElementById("txt-main-title");
const txtMainSubtitle = document.getElementById("txt-main-subtitle");
const thCountry = document.getElementById("th-country");
const thServername = document.getElementById("th-servername");
const thLoad = document.getElementById("th-load");
const thDownload = document.getElementById("th-download");
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
  thCountry.textContent = t.thCountry;
  thServername.textContent = t.thServer;
  thLoad.textContent = t.thLoad;
  thDownload.textContent = t.thAction;
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

async function loadServers() {
  const targetUrl = "https://api.protonvpn.ch/vpn/logicals";
  const proxy = `https://corsproxy.io/?${encodeURIComponent(targetUrl)}`;

  try {
    const res = await fetch(proxy, {
      headers: { "x-pm-appversion": "Other" }
    });
    const data = await res.json();
    serverDataset = data.LogicalServers.filter((s) => s.Status === 1 && s.Tier === 0);
    renderServerList();
  } catch (err) {
    statusCounter.textContent = I18N[currentLang].errConn;
  }
}

function renderServerList() {
  const t = I18N[currentLang];
  const query = searchBox.value.trim().toLowerCase();

  const filtered = serverDataset.filter((s) => {
    return (
      s.Name.toLowerCase().includes(query) ||
      s.ExitCountry.toLowerCase().includes(query) ||
      (s.City && s.City.toLowerCase().includes(query))
    );
  });

  statusCounter.textContent = `${filtered.length} ${t.statusReady}`;
  serversTbody.innerHTML = "";

  filtered.forEach((srv) => {
    const tr = document.createElement("tr");

    const tdCountry = document.createElement("td");
    tdCountry.textContent = `${srv.ExitCountry} - ${srv.City || "Direct"}`;

    const tdName = document.createElement("td");
    const prefix = customPrefix.value.trim() || "ProtonHub";
    tdName.textContent = `${prefix}-${srv.Name}`;

    const tdLoad = document.createElement("td");
    const color = srv.Load < 50 ? "var(--success)" : srv.Load < 80 ? "var(--warning)" : "var(--danger)";
    tdLoad.innerHTML = `
      <div class="load-pill">
        <div class="pill-track">
          <div class="pill-fill" style="width: ${srv.Load}%; background: ${color};"></div>
        </div>
        <span>${srv.Load}%</span>
      </div>
    `;

    const tdAction = document.createElement("td");
    const btn = document.createElement("button");
    btn.className = "dl-btn";
    btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg> ${t.dlBtn}`;
    btn.addEventListener("click", () => exportConfig(srv));
    tdAction.appendChild(btn);

    tr.appendChild(tdCountry);
    tr.appendChild(tdName);
    tr.appendChild(tdLoad);
    tr.appendChild(tdAction);
    serversTbody.appendChild(tr);
  });
}

function exportConfig(srv) {
  const prefix = customPrefix.value.trim() || "ProtonHub";
  const finalFilename = `${prefix}-${srv.Name}`;
  const ip = srv.Servers && srv.Servers[0] ? srv.Servers[0].EntryIP : srv.Domain;

  if (currentProtocol === "wireguard") {
    const pubKey = srv.Servers && srv.Servers[0] ? srv.Servers[0].X25519PublicKey || "" : "";
    const payload = `[Interface]
# Proton Hub Auto Config
PrivateKey = {{CLIENT_WG_PRIVATE_KEY}}
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
auth-user-pass
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