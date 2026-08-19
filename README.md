# KiCad GPS Module PCB Review and Refactor

17.08.2026 tarihli `Refactor PCB GPS Module in KiCAD` Upwork ilanından türetilmiş bağımsız referans/portföy çalışma alanıdır.

## Kaynakta doğrulanan hedef

Mevcut GPS modülü PCB'sinin tamamını incelemek, bulunan sorunları gidermek ve gerekli şematik/yerleşim değişikliklerini KiCad'de yaparak JLCPCB üretimi öncesi işlevsel güveni artırmak.

## Güncel durum

`REFERENCE-SIGNAL-PLANE-TRIAGED / TARGET-INPUT-BLOCKED`.

`septentrio-gnss/mosaicG5-HAT` referans adayı commit `4936e8169b24b613ead996b778399cd3cce22721` üzerinde sabitlenmiş, ana KiCad/BOM/3D dosyaları hash'lenmiş ve KiCad 10.0.5 ile baseline alınmıştır. En önemli teslimat, iki bağımsız DRC koşumunun normalize sinyal/plane JSON'unda byte-identical sonuç vermesidir: proje ilk tekrar üretilebilir D2 kanıtını üretmiştir. P0/P1 kök nedenleri ve sinyal/plane kayıtları ayrıştırılmıştır; aday/ham kayıtlar bulgu toplamına katılmaz. Bunlar erişilemeyen hedef kartın kimliği veya baseline'ı olarak kullanılamaz.

**D2 kanıtının doğrulanmış kaynağı**: yukarıdaki paragrafın atıfta bulunduğu D2 iddiası artık `automation/scripts/reproducibility_check.py` ile CI'da (`.github/workflows/kicad-baseline.yml`, `kicad/kicad:10.0.5` container'ı) fiilen çalıştırılıp doğrulandı — [run #4](https://github.com/kemaldemirag/kicad-gps-module-pcb-review-refactor/actions/runs/32296226526), "D2 reproducibility check PASSED". Kanonikleştirme, gerçek kicad-cli çıktısında gözlemlenen iki değişken alanı (üst seviye `date` zaman damgası ve `drc.json`'daki `violations` dizisinin sırası) hariç tutuyor; bkz. `automation/validation-pipeline.md` Stage 2 ve `docs/source-register.md`.

En yakın kapı: `INPUT-READY`.

Referans içindeki sıradaki bağımsız kapı: `REFERENCE-POWER-ANNOTATION-TRIAGED`.

## Aşama hattı

```text
INPUT-BLOCKED -> INPUT-READY -> BASELINED -> RULES-FROZEN
-> REFACTORED -> VERIFIED -> FAB-READY (koşullu)
-> PROTOTYPE-VALIDATED (koşullu) -> RELEASED
```

## Çalışma alanları

- `hardware`: Kabul edilen KiCad şematik, PCB, kitaplık ve ilgili donanım kaynakları. Kaynak adayı henüz vendored edilmemiştir.
- `docs`: girdi envanteri, açık sorular, kaynak kaydı, bulgular, kural izlenebilirliği ve waiver politikası.
- `automation`: KiCad CLI baseline runner'ı, contract fixture'ı ve salt-okunur signal/plane analiz aracı.
- `manufacturing`: JLCPCB profil ve koşullu fab/PCBA kapıları; sayısal değerler henüz `TBD`'dir.
- `test`: kaynak, baseline, tasarım, otomatik, CAM ve koşullu fiziksel doğrulama planı.
- `media`: yalnız gizlilik/lisans doğrulandıktan sonra yayımlanacak açıklama görselleri.
- `releases`: kanıt seviyesine bağlı release sınıfları; başlangıçta release yoktur.
- `reference`: sabit kaynak commit'i ve SHA-256 bütünlük manifesti.

## Hazırlanan temel belgeler

- `docs/input-inventory.md`
- `docs/current-state-assessment.md`
- `docs/reference-candidate-assessment.md`
- `docs/static-kicad-inventory.md`
- `docs/module-identity.md`
- `docs/antenna-architecture.md`
- `docs/rf-requirements.md`
- `docs/open-questions.md`
- `docs/decision-log.md`
- `docs/source-register.md`
- `docs/review-findings.md`
- `docs/reference-signal-plane-triage.md`
- `docs/d2-reproducibility-record.md`
- `docs/rule-traceability.md`
- `docs/waivers.md`
- `automation/validation-pipeline.md`
- `manufacturing/jlcpcb-profile.md`
- `manufacturing/stackup-candidate.md`
- `test/verification-plan.md`
- `test/environment/preflight.md`
- `releases/release-checklist.md`

## Kapsam sınırı

Gerber/BOM/CPL, JLCPCB ön kontrolü ve fiziksel bring-up koşullu kapsamdır. Fiziksel test olmadan çalışma garantisi veya doğrulanmış RF performansı iddiası verilmez. Exact parça ve stack-up bilgisi olmadan örnek tasarımlardan sayısal RF/DFM kuralı kopyalanmaz.
