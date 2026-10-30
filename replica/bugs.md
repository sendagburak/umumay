# Doğrulanan ve düzeltilen sorunlar

- B01 / S2: Portable ar başlığındaki son `/`, macOS ar'ın üye adını tam
  eşlemesini bozuyordu. `ar -p ... data.tar.gz` ile tekrarlandı; üye adı
  standard Debian biçimine düzeltildi; ar/tar tekrar kontrolü geçti.
- B02 / S2: Uzak AT_SPI_BUS_ADDRESS ve DBUS_STARTER_ADDRESS ilk doğrulama
  sınırında reddedilmiyordu. Test önce başarısız oldu; tüm bilinen D-Bus
  taşıyıcıları Unix ile sınırlandı. Regresyon testi eklendi.

- B03 / test ortamı: minimal Pardus imajı CA/varsayılan SSL yolunu
  içermiyordu. Sertifika doğrulaması açık tutularak bootstrap eklendi.
- B04 / test aracı: eski GTK'de GDK ekran yakalama çağrısı Cairo assertion
  üretiyordu. Normal çizim geçti; yakalama scrot/X11'e taşındı.
- B05 / S2: Pardus21/23 XFCE PowerManager inhibitör yolu eksikti. Gerçek
  servis testi önce başarısız oldu; resmî API adaptörü eklendi ve gerçek
  HasInhibit durumunun true→false değiştiği doğrulandı.

Bilinen açık, tekrarlanmış S1/S2 yoktur. Bu, bekleyen tam ISO/Wayland/
fiziksel donanım testlerinin yerine geçmez; kapsam docs/VALIDATION.md'dedir.
