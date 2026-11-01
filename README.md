<p align="center"><img src="data/icons/128x128/apps/umumay.png" width="96" height="96" alt="Umumay logosu"></p>

# Umumay

**Bilgisayarında çalışır. Bilgilerini yanında tutar.**

Pardus ve Debian için küçük, modüler masaüstü araçları. Sistem kaynaklarını gör,
kurulu paketlerde ara, ekranını süreli uyanık tut ve bağlantılardaki takip
parametrelerini temizle. Hesap açmana, e-posta vermene veya bir sunucuya
bağlanmana gerek yok.

[English](README.en.md) · [İndir / Downloads](https://github.com/sendagburak/umumay/releases)
· [Gizlilik](docs/PRIVACY.md) · [GPL-3.0-or-later](LICENSE)

Umumay bağımsız bir açık kaynak projedir. Resmî Pardus veya TÜBİTAK/ULAKBİM
ürünü değildir. **0.1.4 geliştirme önizlemesidir.** Python 3.9+ ve GTK 3.24
ile Pardus 25, 23 ve 21 ailelerini hedefler. Pardus 21'in dağıtım desteği
sona ermiştir. Uygulama uyumluluğu işletim sistemine güvenlik desteği sağlamaz.

## İçinde neler var?

| Araç | Yaptığı iş |
| --- | --- |
| Sistem | Anlık CPU, bellek, kök disk doluluğu ve çalışma süresi |
| Paketler | Yerel kurulu Debian paketlerinde ad ve sürüm araması |
| Uyanık tut | Oturum destekliyorsa 15–120 dakika boşta kalma/güç tasarrufunu erteleme |
| Bağlantı | Elle girilen URL'den takip parametrelerini yerelde çıkarma |
| Modüller | Araçları açıp kapatma ve isteğe bağlı masaüstü kısayolu oluşturma |

Logo uygulama başlığında, pencere simgesinde, uygulama menüsünde, görev
çubuğunda ve desteklenen bildirim alanında kullanılır. Kısayol için
**Modüller → Masaüstü kısayolu oluştur…** yolunu izle.
Dosya yöneticin isterse kısayola sağ tıklayıp başlatmaya izin vermen gerekir.
GNOME'da bildirim alanı için AppIndicator, masaüstünde dosya simgeleri için
masaüstünün ilgili desteği gerekir. Uygulama bunları kendiliğinden kurmaz.
Pencere kapanınca uygulama ve uyanık tutma isteği kapanır.

Mevcut arayüz normal bir GTK penceresidir. Üst çentikten açılan panel fikri
henüz uygulanmadı. Arayüz Türkçedir; gizlilik metni Türkçe ve İngilizce sunulur.

## Kurulum

[Sürümler](https://github.com/sendagburak/umumay/releases) sayfasından aynı
sürümün `.deb`, kaynak arşivi ve `SHA256SUMS` dosyalarını indir.

```sh
sha256sum -c SHA256SUMS
sudo apt install ./umumay_0.1.4_all.deb
umumay
```

`apt`, eksik bağımlılıkları dağıtım depolarından indirebilir. Tam çevrimdışı
kurulum için bunları önceden sağlamalısın. Önizleme paketi imzasızdır.
SHA256 dosyası bütünlüğü denetler, yayıncı kimliğini doğrulamaz.

Kaynak koddan, kaynak klasörünün içinde:

```sh
sudo apt install python3 python3-gi gir1.2-gtk-3.0 gir1.2-ayatanaappindicator3-0.1
python3 -m umumay
```

Ayatana göstergesi isteğe bağlıdır. Olmadığında X11 bildirim alanı kullanılır.
Uygun alan yoksa araçlar normal pencerede çalışmaya devam eder.

## Bilgilerin nerede kalır?

Ölçümler, paket listesi ve elle girilen bağlantılar uygulamanın belleğinde
işlenir. Bağlantı açılmaz, DNS sorgusu yapılmaz, pano izlenmez. Otomatik
kaydedilen tek bilgi kapalı modüllerin kimlikleridir. İstersen sınırlı bir
JSON raporu ve masaüstü kısayolu kaydedebilirsin. Ağ diski veya bulutla
eşitlenen klasör seçme. İşletim sisteminin eşitlemesini uygulama yönetemez.

Hesap, ödeme, abonelik, analitik, telemetri, hata yükleme, reklam ve otomatik
güncelleme sorgusu yoktur. GitHub'dan indirme, bağımlılık kurulumu ve CI
testleri uygulamanın çalışma zamanından ayrıdır.

[Türkçe bildirim](umumay/privacy_tr.txt) · [English notice](umumay/privacy_en.txt)

## Geliştirme ve test

```sh
python3 -m unittest discover -s tests -v
# Linux üzerinde gerçek GTK testi:
RUN_GTK_TESTS=1 dbus-run-session -- xvfb-run -a python3 -m unittest discover -s tests -v
# Linux üzerinde Debian paketi:
dpkg-buildpackage -us -uc -b
```

GitHub Actions, Debian 11/12/13 ve resmî Pardus 21/23/25 kullanıcı alanlarını
sınar. Çalıştırma konteynerlerinde ağ kapalıdır. Bu kontroller tam Pardus ISO,
GNOME Shell, Wayland ve fiziksel donanım testi yerine geçmez.
[Güncel doğrulama sınırı](docs/VALIDATION.md) ve
[uyumluluk kaynakları](docs/COMPATIBILITY.md) ayrıntıları açıklar.

[Katkı](CONTRIBUTING.md) · [Güvenlik bildirimi](SECURITY.md) ·
[Mimari](docs/ARCHITECTURE.md) · [Logo](docs/BRANDING.md) ·
[Yayın süreci](docs/RELEASE.md) · [Adın hikâyesi](docs/NAME.md)

Ad, Hüma kuşundan ilham alan özgün bir seçimdir. Tarihî bir sözcük varyantı
olduğu iddia edilmez. Vorssaint'in kodu, logosu veya tasarımı kopyalanmadı.
Kod ve beraberindeki logo GPL-3.0-or-later ile sunulur.
