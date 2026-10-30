# İşlev araştırması — 30 Ekim 2026

Ürün: Pardus 25/23/21 kullanıcıları için modüler, tamamen yerel masaüstü araçları.
Ad kullanıcı kararıyla **Umumay**, teknik paket/komut adı `umumay`tir.
Vorssaint portu, fork'u veya resmî Pardus ürünü değildir.

## Kaynaklar ve sınırlar

| Kaynak | Kanıt |
| --- | --- |
| https://github.com/vorssaint/vorssaint-utils/blob/a5da7633e09d0ebbf5b5607c0434ded28a239469/README.md | macOS 14+, Apple Silicon; modül seçimi, sistem ölçümleri, uyanık tutma, bağlantı temizleme dahil özellik açıklamaları |
| Aynı commit'teki LICENSE ve TRADEMARKS.md | Kod GPL-3.0-or-later; marka ve görsel kimlik ayrı. Bizim GPL seçimimiz bağımsız proje kararıdır. |
| https://pardus.org.tr/surumler/ | Güncel masaüstü 25.2; XFCE/GNOME |
| https://pardus.github.io/lifecycle/ | 25→Debian13; 23→Debian12; 21→Debian11 |
| https://pardus.org.tr/pardus-surum-yonetimi/ | Destek takvimi; yaşam döngüsü sayfasıyla tarih farkları var |
| https://github.com/Jakeschincariol/replica-skill/tree/77c9436fb3d18c3d58169efb8caf4fe906b0dc51 | recon/architect/design/build/test/diff yöntemi |

Referans depo `work/reference/` altında indirilmiştir, teslimatın parçası değildir.
Yalnız README, lisans, marka ve gizlilik belgeleri checkout edildi/okundu;
uygulama kodu veya tasarım varlıkları kopyalanmadı. Ekran görüntüsü
ölçümü, gerçek macOS davranış denemesi yapılmadı. Aşağıdaki ekranlar
referans uygulamanın gözlenmiş ekranları değil, özgün Linux tasarımımızdır.
REA becerisi okundu; sunulan REA MCP aracı ve yerel Node/npm yok.
REA analizi veya decompiler sonucu üretilmiş değildir.

## Ekranlar

| ID | Ekran | Amaç | Durumlar |
| --- | --- | --- | --- |
| S01 | Sistem | CPU/RAM/disk/çalışma süresi, aile bilgisi, rapor | ilk örnek, canlı, veri yok, destek dışı aile |
| S02 | Paketler | Kurulu Debian paketlerinde yerel arama | yükleniyor, boş, sonuçlar, araç yok/hata |
| S03 | Uyanık tut | 15/30/60/120 dk ekranın boşta kalmasını engelle | pasif, etkin, izin/servis yok, süre doldu |
| S04 | Bağlantı | Elle girilen URL'den izleme parametresi çıkar | boş, geçerli, hatalı, imzalı URL |
| S05 | Modüller | Sabit modül listesini etkinleştir/kapat | etkin, kapalı, ayar kaydı hatası |

## Akışlar

F01: Aç → Sistem → ilk CPU örneği → canlı değer → yerel JSON raporunu seçerek kaydet.
F02: Paketler → yükleme → arama → eşleşme/boş sonuç; hiçbir paket değişikliği yok.
F03: Uyanık tut → süre → başlat → durum → durdur / süre sonu / pencere kapanışı.
F04: Bağlantı → kullanıcı URL yapıştırır → temizle → sonucu görür; otomatik pano okuması yok.
F05: Modüller → kapat → sayfa/iş durur → yeniden aç → ayar sonraki açılışta korunur.

## Veri modeli ve ölçek

Anlık Snapshot ve Package kayıtları bellekte tutulur. Kalıcı veri yalnız
`settings.json`: şema sürümü ve kapatılan sabit modül kimlikleri. Kimlik,
hesap, ödeme, e-posta, sunucu, analitik ve otomatik güncelleme bağlantısı yok.
5 ekran, 5 akış. En zor kısımlar gerçek masaüstü D-Bus farklılıkları,
Pardus21 eski tabanı ve altı VM'de doğrulamadır. İlk sürüm önizlemedir;
genel kullanıma hazır veya bütün Vorssaint ile eşdeğer olduğu söylenmez.

Ses mikseri, pencere yerleşimi, otomatik pano, ekran yakalama, temizleme,
paket kaldırma ve üçüncü taraf eklenti yükleme bu dilimin dışındadır.
