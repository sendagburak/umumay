# Umumay — doğrulama kapsamı / Validation scope

## 0.1.4 paketleme düzeltmesi — 1 Kasım 2026

Geliştirme notları public kaynak ve ikili paketten çıkarıldı. Kaynak arşivi
tanımlanmış proje kökleriyle sınırlandı. Bir test, örnek ajan dosyası ve
kimlik bilgisi dosyalarını geçici kopyaya ekleyip paket/kaynak dışında
kaldığını doğrular. Örnekler gerçek anahtar içermez. Yerel koşu: 32 geçti,
1 Linux GTK testi atlandı. Bu sürümün native Linux sonuçları
[GitHub Actions](https://github.com/sendagburak/umumay/actions) kaydındadır.
Uygulamanın araçları ve yerel çalışma davranışı değiştirilmedi.

## Tarihî 0.1.3 doğrulaması

31 Ekim / October 2026. Bu sürüm logo, bildirim alanı, masaüstü kısayolu
ve `io.github.sendagburak.umumay` kimliğini ekler.

| Kontrol / Check | Durum / Status |
| --- | --- |
| Python 3.9 çekirdek, CLI, veri sınırı, özel izinler, ağsız çekirdek | Yerelde 32 geçti; 1 Linux GTK testi atlandı |
| Logo ve tüm boyutların .deb içinde olması, masaüstü kimliği | Paket üreten bütünleşme testi geçti |
| Kısayolun 0700 olması, mevcut dosya ve symlink'i ezmemesi | Yerel gerçek dosya testi geçti |
| Güncel Debian/Pardus Linux build/kur/kaldır/GTK ve ağ izi | Altı görev başarılı; run41141196995, commit e1ed7ce |
| Gerçek tam ISO/GNOME Shell/Wayland/fiziksel donanım | Test edilmedi / Not tested |

[0.1.3 CI kaydı](https://github.com/sendagburak/umumay/actions/runs/41141196995)
Pardus 21/23/25 ve Debian 11/12/13 için başarılıdır. Her ailede 32 çekirdek
testi ve ayrıca kurulu uygulamaya karşı gerçek GTK testi geçti. Pardus
görevleri GNOME/XFCE hizmet API'lerini de çalıştırdı. Yayımlanan native .deb
Pardus 25.2 görevinin çıktısıdır; her ailede aynı ikili dosyanın çapraz
kurulduğu iddia edilmez. Yakalanan GTK ağ izinde IP işlemi görülmedi.
Sürüm etiketi ve eşleşen kaynak e1ed7ce commit'inde sabittir. Bu sayfanın
yayın sonrası belge güncellemesi release paketini değiştirmez.

CI'nin her sürümdeki gerçek sonucu GitHub Actions kaydında görülür.
Başarısız veya çalışmamış görev başarılı sayılmaz. macOS'taki GTK atlaması
Linux başarısı değildir. Bildirim alanı görünürlüğü için gerçek GNOME Shell
veya XFCE paneli gerekir. Xvfb'de GTK nesnesinin kurulması görünür panel
kanıtı olarak sunulmaz.

Önceki 0.1.1 sürümü üç resmî Pardus kullanıcı alanında aynı native .deb
ile 31/31 test ve altı gerçek GNOME/XFCE API kontrolünden geçti.
[Değiştirilmeden korunan tarihî kapsam](HISTORICAL_VALIDATION_0.1.1.md).
0.1.2 ise ad değişikliği sonrası yerel test ve kaynak güvenlik incelemesinden
geçti. Bu sonuçlar kendiliğinden 0.1.3'ün doğrulaması sayılmaz.

Pardus VM ve imajları kullanıcı isteğiyle silindi. Bu sürüm için geliştirici
bilgisayarına yeniden indirilmedi. Uzak CI bağımlılık hazırlığı sırasında
imaj indirir. Uygulamanın çalışma zamanında indirme yapılmaz.
