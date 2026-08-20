# Donanım blok diyagramı — mosaicG5 HAT referans tasarımı

Bu diyagram, referans adayı `septentrio-gnss/mosaicG5-HAT` ve öncülü `mosaicHAT` (Septentrio mosaic-X5 tabanlı, aynı kart-seviyesi mimariyi paylaşan açık kaynak Raspberry Pi HAT tasarımı) araştırılarak, Septentrio'nun mosaic donanım kılavuzundaki modül arayüz bilgileriyle birlikte oluşturulmuştur.

## Diyagram

```text
GNSS UYDULARI (GPS · Galileo · GLONASS · BeiDou)
      |
      v  RF sinyali (L1/L5 bantları)
+------------------------------------+
|        AKTİF GNSS ANTENİ           |
+------------------------------------+
      |
      v  SMA konnektör (Amphenol 132203-12)
+------------------------------------+
|      ANTEN BIAS DEVRESİ            |
|                                     |
|  VANT hattı: 3-5.5V                |
|  Aşırı akım eşiği: 150mA           |
|  Kısa devre algılama + kesme       |
+------------------------------------+
      |
      v                    <-- Güç: RPi 5V (GPIO) veya USB 5V
+------------------------------------+     regülatör --> VDD_3V3 (tek hat)
|    SEPTENTRIO mosaic-G5            |
|                                     |
|  Çok bant / çok takımyıldız GNSS   |
|  AIM+ jamming/spoofing koruması    |
|  4x UART (LVTTL, 3'ü HW flow ctrl) |
|  USB arayüzü                       |
|  PPS çıkışı + 2x event timer pini  |
|  22.8 x 16.4mm, 2.2g               |
+------------------------------------+
      |
   +--+---------------+----------------+
   v                   v                v
 COM1                COM2              USB
(RPi'ye sabit)   (FTDI/BT/RS232     (RxTools/WebUI
                  için header)       192.168.3.1)
   |                   |                |
   v                   v                v
+---------+      +-----------+    +---------+
|Raspberry|      |  Harici   |    | Host PC |
|Pi 40-pin|      |  seri     |    |         |
|GPIO     |      |  cihaz    |    |         |
+---------+      +-----------+    +---------+
```

## Blok açıklamaları

- **Aktif GNSS anteni** — RF sinyalini uydulardan alır, SMA (Amphenol 132203-12 tipi) konnektör üzerinden karta bağlanır.
- **Anten bias devresi** — Aktif antene VANT hattından 3–5.5V besleme sağlar; kısa devre durumunda 150mA üzeri akımı algılayıp devreyi keserek modülü korur.
- **Septentrio mosaic-G5** — 22.8 × 16.4 mm, 2.2 g boyutunda çok bantlı/çok takımyıldızlı (GPS, Galileo, GLONASS, BeiDou) GNSS alıcı modülü. AIM+ ile jamming/spoofing koruması sağlar. Tek bir VDD_3V3 hattından çalışır; bu hat karttaki regülatör tarafından RPi'nin 5V GPIO hattından veya USB'den üretilir. Modülde 4 adet UART portu (3'ü donanım akış kontrollü), bir USB arayüzü, PPS çıkışı ve 2 event timer pini bulunur.
- **COM1** — Raspberry Pi'nin 40-pin GPIO header'ındaki UART hattına sabit bağlıdır; ana host iletişimi için kullanılır.
- **COM2** — Ayrı bir header üzerinden dışa açılır; FTDI, Bluetooth veya RS232 dönüştürücü bağlamak için kullanılabilir.
- **USB** — Modülün USB arayüzünü dışa açar; host PC ile veri/yapılandırma (RxTools veya varsayılan WebUI adresi 192.168.3.1 üzerinden) ve bağımsız çalışma modunda güç sağlar.

## Kapsam notu

Bu diyagram referans adayının (`mosaicG5-HAT`) kart-seviyesi mimarisini belgeler; müşterinin gerçek hedef kartının doğrulanmış şeması değildir. Hedef için girdi hâlâ `TARGET-INPUT-BLOCKED` durumunda olduğundan, bu diyagram şu an yalnızca DRC/metodoloji taban çizgisi ve genel mimari referansı amacıyla kullanılmaktadır. Gerçek hedef kart için exact parça ve stack-up bilgisi olmadan buradaki sayısal değerler (VANT aralığı, akım eşiği vb.) doğrudan kopyalanmamalıdır.

## Kaynaklar

- Septentrio mosaic Hardware Manual — mosaic modül ailesinin ortak dahili mimarisi ve arayüzleri
- github.com/septentrio-gnss/mosaicG5-HAT — referans aday deposu
- github.com/septentrio-gnss/mosaicHAT — mosaic-X5 tabanlı öncül tasarım, aynı kart-seviyesi mimariyi paylaşır (SMA: Amphenol 132203-12, KiCad kaynağı doğrulanmıştır)
- septentrio.com mosaic-G5 ürün sayfaları
