# Pardus Çentik 0.1.1 — gerçek test sonuçları

30 Ekim 2026. macOS/Apple Silicon üzerinde yerel Lima 2.2.1, Debian13 ARM64
Linux VM ve Rosetta ile resmî Pardus amd64 kullanıcı alanları çalıştırıldı.
Kaynak haricî test sunucusuna yüklenmedi. İndirmeler hazırlık aşamasındaydı;
uygulama testleri Docker --network none ile çalıştı.

| Kontrol | Pardus21.5 | Pardus23.5 | Pardus25.2 |
| --- | --- | --- | --- |
| Çekirdek/CLI + gerçek GTK/Xvfb | Geçti | Geçti | Geçti |
| Standart Debian build / kur / kaldır | Geçti | Geçti | Geçti |
| Aynı ortak .deb dosyasının kurulumu | Geçti | Geçti | Geçti |
| GTK strace IP bağlantısı | Yok | Yok | Yok |
| Gerçek GNOME inhibit API ve süre sonu | Geçti | Geçti | Geçti |
| Gerçek XFCE inhibit API ve süre sonu | PowerManager: geçti | PowerManager: geçti | ScreenSaver: geçti |

GTK etkin Linux koşusunda 31/31 test geçti. Akış: ilk gizlilik ekranı,
canlı CPU/RAM/disk, gerçek dpkg listesi ve arama, URL temizleme, modül
kapatma ve ayar yazma hatasında switch geri dönüşü. JSON alan beyaz listesi,
symlink reddi ve 0600 izinleri de sınanır. Normal kullanıcı ve kurulu VS
Code Dev Containers 0.469.0 aracından da 31/31 sonuç alındı.

Oturum testi gerçek daemon'dan cookie alır, kontrollü saatle süre sonunu
tetikler; GNOME IsInhibited ve eski XFCE HasInhibit önce true, sonra false
olmalıdır. Son koşular yalnız konteyner içindeki özel D-Bus kullanır;
VM/macOS sistem soketi paylaşılmaz. Fiziksel ekran/kapak/suspend sınanmaz.

## Giderilenler

- Minimal Pardus imajında CA ve varsayılan SSL yolu eksikti. Güvenilir CA
  katmanı/açık CA yolu sağlandı; TLS/GPG doğrulaması kapatılmadı.
- Eski GTK'de GDK ekran yakalama API'si Cairo assertion üretiyordu. Normal
  çizim ayrıca geçti; yakalama scrot/X11 ile düzeltildi.
  [GNOME kaydı](https://discourse.gnome.org/t/screenshot-test-helper-has-issues-with-synchronizing-rendering-assertion-in-cairo-surface-has-mime-data/1568).
- Pardus21/23'ün eski XFCE PowerManager API'si eksikti. Gerçek servis testi
  önce başarısız oldu; adaptör eklenince HasInhibit true→false doğrulandı.
  [Resmî API](https://raw.githubusercontent.com/xfce-mirror/xfce4-power-manager/master/src/org.freedesktop.PowerManagement.Inhibit.xml).
- SVG/erişilebilirlik test bileşenleri ve masaüstü kategorisi tamamlandı.

## Sınırlar

Tam Pardus ISO boot'u, GNOME Shell'in tamamı, Wayland, gerçek GPU, ekran
kilidi/kapak/suspend ve ARM Pardus ayrıca bekliyor. Altı GitHub işi tanımlı;
GitHub'a yükleme veya CI dispatch yapılmadı. Bu sonuçlar tam masaüstü/
çekirdek sertifikası değildir. Paket önizlemedir; yayıncı/marka kontrolü
henüz tamamlanmadı. REA MCP kullanılmadı. Yerel test VM'si iş bitince durdurulur.
