# Kapsam Daraltma — KiCad GPS Module PCB Review and Refactor

**Portföy rolü:** `CONTEXT-BOUND`
**İlk iterasyon amacı:** Müşteri KiCad kaynakları sağlandığında mevcut GPS PCB'sini izlenebilir biçimde incelemek, doğrulanabilen sorunları düzeltmek ve JLCPCB üretim hedefi için kanıt temeli hazırlamak.

## MVP dahil

- KiCad proje sürümü, özel kitaplıklar ve mevcut revizyon için girdi envanteri.
- Şematik ve PCB'nin uçtan uca inceleme bulgu kaydı.
- Kaynak veri sayfaları ve doğrulanmış üretim kurallarına dayalı KiCad düzeltmeleri.
- ERC/DRC sonuçları ve gerekçeli waiver kaydı.
- GPS parçası/anten/stack-up sağlanırsa RF keepout, matching/bias, besleme hattı ve topraklama incelemesi.
- Footprint, polarite, pin-1, pad ve montaj yönü kontrolleri.
- Değişiklik–bulgu–kanıt izlenebilirliği ve son KiCad kaynak arşivi.

## Koşullu kapsam

- Gerber ve drill üretimi.
- PCBA için BOM/CPL ve JLCPCB parça eşleştirmesi.
- JLCPCB çevrimiçi ön kontrol/quote doğrulaması.
- Fiziksel prototip bring-up ve GPS performans testleri.

Bu maddeler ancak müşteri açıkça ister, gerekli girdileri sağlar ve kapsamı onaylarsa etkinleşir.

## Kapsam dışı

- Kaynakta istenmeyen firmware geliştirme.
- Anten odası, EMC/ESD veya ürün sertifikasyonu.
- Sağlanmayan parça numarası, stack-up veya ölçüm sonuçlarının uydurulması.
- Fiziksel test olmadan "garantili çalışır" veya RF performansı doğrulanmış iddiası.

## Bitti ölçütü

Girdiler eksiksiz açılmalı; her değişiklik bulgu ve kaynakla eşleşmeli; açıklanamayan ERC/DRC ihlali kalmamalı; footprint/DFM kontrolleri kaydedilmeli; onaylı kapsamın KiCad kaynakları ve doğrulama raporu aynı sürüm etiketiyle paketlenmelidir. Üretim paketi veya prototip testi yalnız koşullu kapsam etkinleşirse bitti ölçütüne eklenir.
