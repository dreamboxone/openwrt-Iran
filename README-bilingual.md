# OpenWrt for Google WiFi AC-1304 + Passwall2

<div dir="rtl" align="right">

## فارسی

این پروژه یک نسخه سفارشی از آخرین انتشار رسمی و پایدار **OpenWrt** برای روتر
**Google WiFi AC-1304 (Gale)** تولید می‌کند. در این نسخه، **Passwall2** و قانون
تفکیک ترافیک ایران از قبل درون firmware قرار گرفته‌اند؛ بنابراین پس از نصب یا
ارتقای OpenWrt نیازی به نصب مجدد Passwall2 نیست.

### ویژگی‌ها

- استفاده از آخرین نسخه رسمی و پایدار OpenWrt؛ نسخه‌های Snapshot و RC انتخاب نمی‌شوند.
- نصب خودکار Passwall2 و ابزارهای موردنیاز آن.
- تفکیک دامنه‌ها و آدرس‌های IP ایران و هدایت مستقیم آن‌ها بدون عبور از پراکسی.
- قرار دادن داده‌های GeoIP و GeoSite ایران در firmware.
- ارائه هم‌زمان فایل‌های `factory.bin` و `sysupgrade.bin`.
- بررسی دوره‌ای نسخه‌های جدید OpenWrt و Passwall2 و ساخت خودکار firmware جدید.
- ارائه فایل `sha256sums` برای بررسی سلامت فایل‌های دانلودشده.

### انتخاب فایل مناسب

#### فایل Factory

اگر OpenWrt هنوز روی روتر نصب نشده است، از فایلی استفاده کنید که نام آن به
`factory.bin` ختم می‌شود.

برای نصب اولیه به تجهیزات و مراحل مخصوص Google WiFi نیاز دارید. راهنمای نصب را
در [صفحه رسمی Google WiFi در وب‌سایت OpenWrt](https://openwrt.org/toh/google/wifi)
مطالعه کنید.

#### فایل Sysupgrade

اگر OpenWrt از قبل روی روتر نصب است و فقط می‌خواهید آن را ارتقا دهید، از فایلی
استفاده کنید که نام آن به `sysupgrade.bin` ختم می‌شود.

فایل را به پوشه `/tmp/` روتر منتقل کنید و سپس از طریق SSH اجرا کنید:

```sh
cd /tmp
sysupgrade openwrt-*-sysupgrade.bin
```

پس از اجرای دستور، روتر راه‌اندازی مجدد می‌شود. تا پایان عملیات، برق دستگاه را
قطع نکنید.

### آموزش ویدیویی

[مشاهده آموزش نصب در YouTube](https://www.youtube.com/watch?v=08vnI9CZFlM&t=12s)

### هشدار

نصب firmware سفارشی ممکن است با خطر خرابی یا از دست رفتن تنظیمات همراه باشد.
مسئولیت نصب و استفاده از فایل‌های این پروژه بر عهده کاربر است. پیش از ارتقا از
تنظیمات مهم خود نسخه پشتیبان تهیه کنید و حتماً فایل متناسب با وضعیت دستگاه را
انتخاب کنید.

### تشکر و قدردانی

با سپاس از توسعه‌دهندگان و مشارکت‌کنندگان پروژه
[OpenWrt](https://github.com/openwrt/openwrt) برای توسعه سیستم‌عامل آزاد OpenWrt،
و توسعه‌دهندگان و مشارکت‌کنندگان
[Passwall2](https://github.com/Openwrt-Passwall/openwrt-passwall2) برای توسعه
Passwall2.

</div>

---

<div dir="ltr" align="left">

## English

This project builds a customized image based on the latest official stable
**OpenWrt** release for the **Google WiFi AC-1304 (Gale)**. **Passwall2** and
the Iran traffic-routing rule are embedded in the firmware, so Passwall2 does
not need to be reinstalled after installing or upgrading OpenWrt.

### Features

- Uses the latest official stable OpenWrt release; Snapshot and RC builds are excluded.
- Includes Passwall2 and its required components.
- Routes Iranian domains and IP addresses directly without sending them through the proxy.
- Embeds Iran GeoIP and GeoSite data in the firmware.
- Publishes both `factory.bin` and `sysupgrade.bin` images.
- Periodically checks for new OpenWrt and Passwall2 releases and builds updated firmware automatically.
- Publishes a `sha256sums` file for download integrity verification.

### Choosing the correct image

#### Factory image

If OpenWrt is not installed on the router, use the file whose name ends with
`factory.bin`.

The initial installation requires the Google WiFi-specific equipment and
procedure. Read the
[official OpenWrt Google WiFi installation guide](https://openwrt.org/toh/google/wifi)
before proceeding.

#### Sysupgrade image

If the router already runs OpenWrt and you only want to upgrade it, use the
file whose name ends with `sysupgrade.bin`.

Copy the file to `/tmp/` on the router and run the following commands over SSH:

```sh
cd /tmp
sysupgrade openwrt-*-sysupgrade.bin
```

The router will reboot after the command is executed. Do not disconnect power
until the upgrade has completed.

### Video tutorial

[Watch the installation tutorial on YouTube](https://www.youtube.com/watch?v=08vnI9CZFlM&t=12s)

### Warning

Installing custom firmware can damage the device or erase its configuration.
You are responsible for installing and using files from this project. Back up
important settings before upgrading and make sure that you select the image
appropriate for the current state of your router.

### Acknowledgements

Special thanks to the developers and contributors of
[OpenWrt](https://github.com/openwrt/openwrt) for creating and maintaining the
OpenWrt operating system, and to the developers and contributors of
[Passwall2](https://github.com/Openwrt-Passwall/openwrt-passwall2) for creating
and maintaining Passwall2.

</div>
