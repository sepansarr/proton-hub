<div align="center">
  
# 🛡️ Proton Hub | پروتون هاب

**ژنراتور پیشرفته و خودکار کانفیگ‌های رسمی Proton VPN**

[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)
[![Update](https://img.shields.io/badge/Auto_Sync-Active-success.svg)]()
[![Proton](https://img.shields.io/badge/ProtonVPN-Official_API-blue.svg)]()

[English](#-english) • [پارسی](#-پارسی)

</div>

---

<h2 id="-پارسی">🦁 پارسی</h2>

سامانه‌ای مدرن و متن‌باز برای ساخت، بهینه‌سازی و دریافت کانفیگ‌های رسمی سرورهای رایگان Proton VPN با استانداردهای رسمی WireGuard و OpenVPN.

این سامانه وضعیت سلامت سرورها و درصد بار ترافیکی زنده را هر ۶ ساعت یک‌بار همگام‌سازی کرده و در ابتدای هر ماه میلادی اطلاعات احراز هویت اتصال را به‌روزرسانی می‌کند.

### ✨ امکانات و مشخصات فنی

* 🚀 **تولید کانفیگ استاندارد:** خروجی پروتکل WireGuard شامل آدرس‌های دوگانه IPv6 و PersistentKeepalive، و خروجی OpenVPN شامل کلیدهای tls-crypt و گواهی ریشه رسمی.
* 📊 **محاسبه بار زنده شبکه:** نمایش درصد لود واقعی هر سرور بر اساس داده‌های مستقیم زیرساخت Proton VPN.
* 🌍 **دسته‌بندی منظم کشوری:** نمایش تفکیک‌شده سرورها همراه با پرچم کشورها و پنل‌های آکاردئونی جمع‌شونده.
* 🌓 **واسط کاربری مدرن:** مجهز به کلید کپسولی تغییر حالت تیره و روشن به سبک iOS و دکمه تازه‌سازی سریع داده‌ها.
* ✏️ **شخصی‌سازی:** قابلیت اعمال پیشوند دلخواه روی نام تمامی فایل‌های دانلودی.

### ⚙️ متغیرهای مورد نیاز در گیت‌هاب (Secrets)

پروژه به‌صورت استاتیک روی **GitHub Pages** میزبانی می‌شود. متغیرهای زیر را در مسیر `Settings > Secrets and variables > Actions` مخزن ثبت کنید:

| نام متغیر | توضیحات |
| :--- | :--- |
| `PROTON_COOKIE` | کوکی احراز هویت وب‌سایت پروتون |
| `PROTON_UID` | شناسه یکتای نشست (`x-pm-uid`) |
| `PROTON_USER` | نام کاربری اختصاصی OpenVPN |
| `PROTON_PASS` | کلمه عبور اختصاصی OpenVPN |

### ☕ حمایت مالی (Donate)

جهت پشتیبانی از نگهداری سرورها و استمرار توسعه این ابزار می‌توانید از آدرس‌های زیر استفاده فرمایید:

| شبکه / ارز | آدرس ولت |
| :--- | :--- |
| **USDT (TRC-20) / TRX** | `TKMdxppKeBSDYkaLtBYi1qT3WH4x2y3TAv` |
| **USDT (TON) / TON** | `UQACW49SRyUT-_1fRg_VArfg5oHKMlj97ZqSd9dpHHTZrKy-` |
| **USDT (BEP-20) / BNB** | `0xcA532AC0ef4264002798A2e2ab83eBf41ecC18B6` |

---

<h2 id="-english">🇬🇧 English</h2>

An open-source dashboard engineered to generate, optimize, and export official Proton VPN free server configs using official WireGuard and OpenVPN standards.

Automated via GitHub Actions to refresh server load metrics every 6 hours and rotate connection credentials on the 1st of every month.

### ✨ Key Features

* 🚀 **Official Configuration Standard:** WireGuard profiles featuring dual-stack IPv6 endpoints and keepalive timers; OpenVPN profiles bundled with official Root CA and `tls-crypt` blocks.
* 📊 **Real-Time Server Load:** Live network utilization directly parsed from Proton's infrastructure APIs.
* 🌍 **Collapsible Country Groups:** Structured country accordions logically labeled with national flags.
* 🌓 **Refined Aesthetics:** Sleek iOS-style theme switch, live refresh button, and fully responsive layout.
* ✏️ **Config Renaming:** Dynamic custom prefix application across all exported filenames.

### ⚙️ Deployment & Environment Secrets

Hosted statically via **GitHub Pages**. Configure the following repository secrets under `Settings > Secrets and variables > Actions`:

| Secret Name | Description |
| :--- | :--- |
| `PROTON_COOKIE` | Proton web session cookie |
| `PROTON_UID` | Session identifier (`x-pm-uid`) |
| `PROTON_USER` | Dedicated OpenVPN username |
| `PROTON_PASS` | Dedicated OpenVPN password |

### ☕ Support & Donations

To support the continuous maintenance and updates of this open project:

| Network / Coin | Wallet Address |
| :--- | :--- |
| **USDT (TRC-20) / TRX** | `TKMdxppKeBSDYkaLtBYi1qT3WH4x2y3TAv` |
| **USDT (TON) / TON** | `UQACW49SRyUT-_1fRg_VArfg5oHKMlj97ZqSd9dpHHTZrKy-` |
| **USDT (BEP-20) / BNB** | `0xcA532AC0ef4264002798A2e2ab83eBf41ecC18B6` |

---

<div align="center">
  <b>سلب مسئولیت / Disclaimer</b><br>
  این پروژه مستقل بوده و هیچ‌گونه وابستگی تجاری یا رسمی به شرکت Proton AG ندارد.<br>
  This independent project is not affiliated with, authorized, or endorsed by Proton AG.
</div>
