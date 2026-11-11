# Umumay X11 çentik prototipi (geliştirme dalı)

**Durum:** `main` dalına birleştirilmiş deneysel kaynak kod; yayımlanan 0.1.4 .deb içinde bulunmaz.
**Amaç:** Fare ile açılan, ekranın üst ortasında duran küçük bir çentik. Normal
760×560 uygulama penceresi ürünün ana arayüzü değildir.

## Etkileşim
- Açılışta 156×30 piksel genişlikte üst-orta bir tutamak.
- Üzerinde yaklaşık 95 ms bekleyen fareyle 640×480 sınırlı panel açılır.
- Fare ayrıldığında 430 ms gecikmeyle kapanır; içeride dolaşırken kapanmaz.
- Tutamağa tıklama paneli sabitler; Escape sabitlemeyi kaldırıp kapatır.
- Panel içindeki **× Kapat** uygulamayı *gerçekten kapatmaz*: kullanılabilir
  bildirim alanı varsa Umumay simgesine gizler.
- İlk gizlenmede yerel masaüstü bildirimi gönderilir; bildirime tıklayarak
  eylem yapılacağı iddia edilmez. Simge menüsü: **Göster**, **Tamamen çık**.
- Desteklenen bildirim alanı yoksa gizlenip ulaşılamaz olmak yerine
  görünür uyarı verir ve açık kalır.
- Modüller > **Oturum açıldığında başlat** varsayılan kapalıdır.
  Kullanıcı etkinleştirince `~/.config/autostart/io.github.sendagburak.umumay.desktop`
  oluşturulur; devre dışı bırakılınca yalnız Umumay'ın kendi girdisi silinir.

## Platform sınırları
- XFCE/X11 ve GNOME/Wayland (XWayland üzerinden) desteklenir.
- GNOME Wayland oturumunda `GDK_BACKEND=x11` üzerinden XWayland çentik modu kullanılır.
  GNOME masaüstünde üst panel dikkate alınarak çentik üst barın hemen altına hizalanır.
- X11'de üst panel/çoklu monitör/ekran ölçekleme ve tray host durumu farklı
  sistemlerde değişebilir. Etkili son kullanıcı desteği, tam ISO üzerinde test
  edilmeden ilan edilmeyecek.
- Otomatik ağ isteği, sunucu, telemetry, ayrıcalıklı servis yok.
- Uygulama tekil `GApplication` kimliği kullanır; oturumdaki ikinci başlatma
  mevcut çalışan çentiği yeniden açmayı hedefler.

## Gerçek Pardus yayın kapısı
- [ ] Pardus 21 XFCE/X11: üst orta tutamak, hover, kapanma, bildirim alanı, autostart
- [ ] Pardus 23 XFCE/X11: aynı işlemler
- [ ] Pardus 25 XFCE/X11: aynı işlemler
- [ ] X11 çoklu monitör / farklı ölçek / üst panel çakışması
- [ ] Panelden çıkış, uygulamayı yeniden açma, oturum açılışından tekrar başlatma
- [ ] GNOME/Wayland için ayrı uygulanabilir çözüm ve gerçek testler
- [ ] Kullanılabilirlik, erişilebilirlik, CPU ve RAM izleme

CI başarısı deneysel çentiğin gerçek masaüstünde doğrulandığı anlamına gelmez.
