# Donanım blok diyagramı — mosaicG5 HAT referans tasarımı

Bu diyagram, referans adayı `septentrio-gnss/mosaicG5-HAT` ve öncülü `mosaicHAT` (Septentrio mosaic-X5 tabanlı, aynı kart-seviyesi mimariyi paylaşan açık kaynak Raspberry Pi HAT tasarımı) araştırılarak, Septentrio'nun mosaic donanım kılavuzundaki modül arayüz bilgileriyle birlikte oluşturulmuştur.

## Diyagram

```mermaid
flowchart TB
    SAT["GNSS uyduları<br/>GPS · Galileo · GLONASS · BeiDou"]
    ANT["Aktif GNSS anteni (harici)"]

    subgraph HAT["mosaicG5 HAT PCB — 40-pin Raspberry Pi HAT"]
        direction TB
        SMA["SMA anten konnektörü"]
        BIAS["Anten bias devresi<br/>VANT 3–5.5V, aşırı akım koruması (150mA üzeri)"]
        MOD["Septentrio mosaic-G5<br/>GNSS alıcı modülü"]
        PWR["Güç regülasyonu<br/>→ VDD_3V3 (tek 3.3V hat)"]
        USBC["USB konnektörü"]
        COM1P["COM1 header<br/>(RPi'ye sabit bağlantı)"]
        COM2P["COM2 header<br/>(FTDI / BT / RS232 için)"]
        TIME["PPS çıkışı + 2x event timer pini"]
        LED["Durum LED'leri"]
    end

    RPI["Raspberry Pi<br/>40-pin GPIO header"]
    PC["Host PC<br/>RxTools / WebUI"]
    EXT["Harici seri cihaz<br/>(FTDI / BT / RS232)"]

    SAT -.-> ANT
    ANT --> SMA
    SMA --> BIAS
    BIAS --> MOD
    RPI ==>|"5V güç"| PWR
    USBC ==>|"5V güç, bağımsız çalışma"| PWR
    PWR --> MOD
    COM1P <--> MOD
    RPI <-->|"COM1 UART"| COM1P
    COM2P <--> MOD
    EXT <-->|"COM2 UART"| COM2P
    USBC <--> MOD
    PC <-->|"USB"| USBC
    MOD --> TIME
    MOD --> LED
```

## Blok açıklamaları

- **mosaic-G5 modülü** — Septentrio'nun çok bantlı, çok takımyıldızlı (GPS, Galileo, GLONASS, BeiDou) GNSS alıcı modülü; kartın çekirdeği. Tek bir 3.3V besleme hattından (VDD_3V3) çalışır.
- **Anten bias devresi** — Aktif GNSS antenine VANT pini üzerinden 3–5.5V besleme sağlar; kısa devre durumunda 150mA üzeri akımı algılayıp modülü korur.
- **Güç regülasyonu** — Raspberry Pi'nin 40-pin header'ından veya USB konnektöründen gelen 5V'u modülün tek besleme hattı olan VDD_3V3'e indirger.
- **COM1 / COM2** — Modülün seri portları. COM1 sabit olarak Raspberry Pi GPIO header'ındaki UART hattına bağlıdır; COM2 ayrı bir header üzerinden dışa açılır ve FTDI, Bluetooth veya RS232 dönüştürücü bağlamak için kullanılabilir.
- **USB konnektörü** — Modülün USB arayüzünü dışa açar; hem veri/yapılandırma (RxTools, WebUI) hem de bağımsız çalışma modunda güç sağlayabilir.
- **PPS + event timer** — Saniye-başı darbe (PPS) çıkışı ve 2 adet olay zamanlayıcı girişi; zamanlama/senkronizasyon uygulamaları için.
- **Durum LED'leri** — Modülün ve kartın çalışma durumunu gösteren gösterge LED'leri.
- **Mekanik** — HAT standardına uygun 4 montaj deliği (diyagrama dahil edilmedi, sinyal/güç akışına dahil olmayan mekanik bir unsur).

## Kapsam notu

Bu diyagram referans adayının (`mosaicG5-HAT`) kart-seviyesi mimarisini belgeler; müşterinin gerçek hedef kartının doğrulanmış şeması değildir. Hedef için girdi hâlâ `TARGET-INPUT-BLOCKED` durumunda olduğundan, bu diyagram şu an yalnızca DRC/metodoloji taban çizgisi ve genel mimari referansı amacıyla kullanılmaktadır. Gerçek hedef kart için exact parça ve stack-up bilgisi olmadan buradaki sayısal değerler (VANT aralığı, akım eşiği vb.) doğrudan kopyalanmamalıdır.

## Kaynaklar

- Septentrio mosaic Hardware Manual — mosaic modül ailesinin ortak dahili mimarisi ve arayüzleri
- github.com/septentrio-gnss/mosaicG5-HAT — referans aday deposu
- github.com/septentrio-gnss/mosaicHAT — mosaic-X5 tabanlı öncül tasarım, aynı kart-seviyesi mimariyi paylaşır
- septentrio.com mosaic-G5 ürün sayfaları
