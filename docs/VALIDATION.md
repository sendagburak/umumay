# Umumay 0.1.3 — doğrulama kapsamı / Validation scope

31 Ekim / October 2026. Bu sürüm logo, bildirim alanı, masaüstü kısayolu
ve `io.github.sendagburak.umumay` kimliğini ekler.

| Kontrol / Check | Durum / Status |
| --- | --- |
| Python 3.9 çekirdek, CLI, veri sınırı, özel izinler, ağsız çekirdek | Yerelde 32 geçti; 1 Linux GTK testi atlandı |
| Logo ve tüm boyutların .deb içinde olması, masaüstü kimliği | Paket üreten bütünleşme testi geçti |
| Kısayolun 0700 olması, mevcut dosya ve symlink'i ezmemesi | Yerel gerçek dosya testi geçti |
| Güncel Debian/Pardus Linux build/kur/kaldır/GTK ve ağ izi | GitHub Actions sonucu ile ayrıca doğrulanır |
| Gerçek tam ISO/GNOME Shell/Wayland/fiziksel donanım | Test edilmedi / Not tested |

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
