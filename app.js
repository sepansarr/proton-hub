const I18N = {
    fa: {
        title: "پروتون هاب",
        search: "جستجوی سرورها...",
        loading: "در حال بارگذاری داده‌ها...",
        prefix: "پیشوند:",
        syncing: "در حال همگام‌سازی...",
        synced: "همگام‌سازی شد",
        wg: "وایرگارد",
        udp: "اوپن وی‌پی‌ان UDP",
        tcp: "اوپن وی‌پی‌ان TCP"
    },
    en: {
        title: "Proton Hub",
        search: "Search servers...",
        loading: "Loading data...",
        prefix: "Prefix:",
        syncing: "Syncing...",
        synced: "Synced",
        wg: "WireGuard",
        udp: "OpenVPN UDP",
        tcp: "OpenVPN TCP"
    }
};

let currentLang = "fa";
let serversData = [];
let liveLoads = {};

function updateLanguage() {
    document.documentElement.lang = currentLang;
    document.documentElement.dir = currentLang === "fa" ? "rtl" : "ltr";
    document.getElementById("lbl-title").textContent = I18N[currentLang].title;
    document.getElementById("search-input").placeholder = I18N[currentLang].search;
    document.getElementById("lbl-prefix").textContent = I18N[currentLang].prefix;
    document.getElementById("proto-wg").textContent = I18N[currentLang].wg;
    document.getElementById("proto-udp").textContent = I18N[currentLang].udp;
    document.getElementById("proto-tcp").textContent = I18N[currentLang].tcp;
    const loadingEl = document.getElementById("loading-indicator");
    if(loadingEl) {
        loadingEl.textContent = I18N[currentLang].loading;
    }
}

document.getElementById("lang-toggle").addEventListener("click", () => {
    currentLang = currentLang === "fa" ? "en" : "fa";
    document.getElementById("lang-toggle").textContent = currentLang === "fa" ? "EN" : "FA";
    updateLanguage();
    renderServers();
});

document.getElementById("theme-toggle").addEventListener("click", () => {
    const root = document.documentElement;
    if (root.getAttribute("data-theme") === "dark") {
        root.setAttribute("data-theme", "light");
    } else {
        root.setAttribute("data-theme", "dark");
    }
});

function fetchLiveMetrics() {
    document.getElementById("sync-status").textContent = I18N[currentLang].syncing;
    fetch("https://api.allorigins.win/get?url=" + encodeURIComponent("https://api.protonvpn.ch/vpn/loads"))
        .then(res => res.json())
        .then(data => {
            const parsedData = JSON.parse(data.contents);
            const loads = parsedData.LogicalServers;
            loads.forEach(server => {
                liveLoads[server.Name] = server.Load;
            });
            document.getElementById("sync-status").textContent = I18N[currentLang].synced;
            renderServers();
        })
        .catch(() => {
            document.getElementById("sync-status").textContent = "Sync Failed";
            renderServers();
        });
}

function renderServers() {
    const container = document.getElementById("server-list");
    container.innerHTML = "";
    const query = document.getElementById("search-input").value.toLowerCase();
    const filtered = serversData.filter(s => s.name.toLowerCase().includes(query));

    filtered.forEach(server => {
        const load = liveLoads[server.name] || server.load || 0;
        const div = document.createElement("div");
        div.className = "accordion-item";
        div.innerHTML = `
            <div class="accordion-header">
                <span>${server.name}</span>
                <span>Load: ${load}%</span>
            </div>
            <div class="accordion-body">
                <button class="dl-btn" data-type="wg">WG</button>
                <button class="dl-btn" data-type="udp">UDP</button>
                <button class="dl-btn" data-type="tcp">TCP</button>
            </div>
        `;
        container.appendChild(div);
        
        const header = div.querySelector(".accordion-header");
        header.addEventListener("click", () => {
            div.classList.toggle("active");
        });

        const btns = div.querySelectorAll(".dl-btn");
        btns.forEach(btn => {
            btn.addEventListener("click", (e) => {
                e.stopPropagation();
                generateConfig(server, btn.getAttribute("data-type"));
            });
        });
    });
}

function generateConfig(server, type) {
    const prefix = document.getElementById("prefix-input").value || "Proton";
    let content = "";
    let ext = "";
    if (type === "wg") {
        const pubKey = server.pubkey || "INSERT_PUBLIC_KEY_HERE";
        content = "[Interface]\nPrivateKey = INSERT_PRIVATE_KEY_HERE\nAddress = 10.2.0.2/32\nDNS = 10.2.0.1\n\n[Peer]\nPublicKey = " + pubKey + "\nEndpoint = " + server.ip + ":51820\nAllowedIPs = 0.0.0.0/0";
        ext = ".conf";
    } else {
        content = "client\ndev tun\nproto " + type + "\nremote " + server.ip + " 1194\nresolv-retry infinite\nnobind\ncipher AES-256-GCM\nauth SHA512\nverb 3";
        ext = ".ovpn";
    }
    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = prefix + "-" + server.name + ext;
    a.click();
    URL.revokeObjectURL(url);
}

document.getElementById("search-input").addEventListener("input", renderServers);

const initInterval = setInterval(() => {
    if (window.STATIC_SERVERS) {
        clearInterval(initInterval);
        serversData = window.STATIC_SERVERS;
        updateLanguage();
        fetchLiveMetrics();
        setInterval(fetchLiveMetrics, 60000);
    }
}, 500);
