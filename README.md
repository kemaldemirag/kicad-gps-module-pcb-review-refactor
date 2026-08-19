# KiCad GPS Module PCB Review and Refactor

17.08.2026 tarihli `Refactor PCB GPS Module in KiCAD` Upwork ilanından türetilmiş bağımsız referans/portföy çalışma alanıdır. **Gerçek bir müşteri girdisi henüz yok**; bu repo, o girdi geldiğinde kullanılacak inceleme sürecini gerçek bir açık kaynak GPS PCB'si (`septentrio-gnss/mosaicG5-HAT`) üzerinde uçtan uca çalışır durumda gösteriyor.

## Bu çalışma neyi gösteriyor

- **Bağımsız doğrulanmış kaynak**: referans PCB projesi hash'lenip commit'e sabitlendi, iddia edilen her ayrıntı (commit, KiCad sürümü, lisans) bu oturumda yeniden kontrol edildi.
- **Gerçek, tekrarlanabilir CI**: `kicad-cli 10.0.5` içeren bir container'da ERC/DRC gerçekten çalışıyor; iki bağımsız koşum birebir aynı sonucu veriyor (D2 kanıtı — bkz. [CI çalıştırmaları](https://github.com/kemaldemirag/kicad-gps-module-pcb-review-refactor/actions)), iddia değil, tekrarlanabilir kanıt.
- **Otomatik özet çıkarımı**: ERC/DRC ham çıktısı `by_type`/`by_severity` dökümüne indirgeniyor ve kalıcı kanıt olarak commit ediliyor (`evidence/`) — CI logu silinse bile kaybolmuyor.
- **Net kapsam sınırları**: hiçbir sayısal RF/DFM kuralı uydurulmuyor, hiçbir mühendislik yargısı (bu bulgu "kritik"tir gibi) otomatik üretilmiyor; bunlar insan incelemesi gerektiriyor ve öyle işaretleniyor.

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

- `hardware/reference/mosaicG5-HAT`: vendored referans KiCad projesi (bkz. `docs/source-register.md` için hash manifesti, `ATTRIBUTION.md` için lisans). Hedef müşteri kartı için ayrı bir yer henüz yok (`INPUT-BLOCKED`).
- `docs`: kaynak kaydı, karar günlüğü, gate/süreç sözlüğü. Girdi envanteri, RF gereksinimleri, bulgular gibi geri kalanı gerçek müşteri girdisi bekliyor.
- `automation`: KiCad CLI ortam pini, baseline runner, D2 reproducibility check, signal/plane analiz aracı — dördü de CI'da çalışır durumda.
- `manufacturing`: JLCPCB profil ve koşullu fab/PCBA kapıları; henüz boş, sayısal değerler `TBD`.
- `test`: kaynak, baseline, tasarım, otomatik, CAM ve koşullu fiziksel doğrulama planı; henüz boş.
- `media`: yalnız gizlilik/lisans doğrulandıktan sonra yayımlanacak açıklama görselleri; henüz boş.
- `releases`: kanıt seviyesine bağlı release sınıfları; başlangıçta release yoktur.
- `evidence`: CI'da üretilen gerçek ERC/DRC ham sayı dökümü, kalıcı kanıt olarak.

## Var olan belgeler

Aşağıdakiler gerçekten repoda mevcut (bu liste, geçmişte burada olup henüz
yazılmamış ~15 belgeyi vaat eden bir listenin yerini aldı — o belgeler
`INPUT-BLOCKED` durumu ve gerçek müşteri girdisi olmadan yazılamaz,
yazılırsa uydurma olur):

- `docs/decision-log.md` — kabul edilmiş/önerilen kararlar (DEC-006…009)
- `docs/source-register.md` — referans kaynağın hash/commit kaydı
- `docs/label-dictionary.md`, `docs/gates/g-annot-contract.md`,
  `docs/g-debt-corrections.md`, `docs/proposed-backlog.md` — süreç/gate
  sözlüğü ve iş listesi
- `automation/validation-pipeline.md` — pipeline'ın 4 aşaması, hangilerinin
  gerçekten çalıştığı
- `automation/environment.md` — pinlenmiş KiCad CLI ortamı
- `evidence/reference-erc-drc-summary.{json,md}` — gerçek ERC/DRC ham
  sayıları

Henüz yazılmamış (müşteri girdisi veya insan mühendislik kararı bekliyor):
girdi envanteri, RF gereksinimleri, kural izlenebilirliği, waiver politikası,
imalat profili, doğrulama planı, release checklist.

## Kapsam sınırı

Gerber/BOM/CPL, JLCPCB ön kontrolü ve fiziksel bring-up koşullu kapsamdır. Fiziksel test olmadan çalışma garantisi veya doğrulanmış RF performansı iddiası verilmez. Exact parça ve stack-up bilgisi olmadan örnek tasarımlardan sayısal RF/DFM kuralı kopyalanmaz.
