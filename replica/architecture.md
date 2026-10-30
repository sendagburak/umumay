# Umumay — mimari ve modül öncelikleri

## Kararlar

Python >=3.9 + sistem PyGObject + GTK >=3.24 seçildi. Alternatifler:
GTK4/libadwaita 21'de ek bağımlılık/backport yükü; Qt/PySide daha fazla
dağıtım bağımlılığı getirir. GTK3 ortak taban ve XFCE/GNOME görünümü için
seçildi. Hiçbiri macOS API'lerini taşımayı gerektirmez.

```
GTK 3 pencere / sabit modül kataloğu
          │
     Python çekirdek ── settings.json (0600, atomik)
       │      │
 /proc + /etc dpkg-query (salt okunur, zaman aşımı)
          │
 ekran boşta kalma hizmeti (oturum D-Bus, süreli inhibit)
```

`core.py`: saf ayrıştırma, sürüm tanıma, ölçüm, paket sorgusu.
`storage.py`: doğrulanan sabit modül ayarları ve sınırlı rapor ihracı.
`links.py`: ağ bağlantısı olmadan URL temizleme.
`awake.py`: zaman sınırı ve kapanış; GTK'den bağımsız denetleyici.
`desktop.py`: Gio D-Bus adaptörü; freedesktop ScreenSaver ve GNOME
SessionManager arka uçları. Manuel kilit/kapak kapama engellenmez.
`ui.py`: GTK arayüzü; yavaş sorgular iş parçacığında, GTK güncellemeleri ana
döngüde; kapalı modülün sonuçları temizlenir. Başlamış paket sorgusu 10 saniyelik
sınır içinde biter ve sonucu atılır. Dinamik Python eklentisi yok.
`__main__.py`: GUI veya GTK gerektirmeyen `--report`, `--version` komutları.

P0 sistem ölçümleri, modül tercihleri ve yerel rapor. P1 paket araması,
süreli uyanık tutma, elle URL temizleme. P2 PulseAudio/PipeWire ses mikseri
ve kullanıcıya ait başlangıç girdileri. P3 pano/ekran/pencere araçları;
Wayland izin modeli ayrıca tasarlanacak. Temizlik ve kaldırma için önizleme,
geri alma ve işlem bazında polkit tasarlanmadan yetkili yardımcı eklenmez.

## Güvenlik sınırı

Uygulama normal kullanıcı olarak çalışır; sudo, setuid, polkit kuralı ve
arka plan daemon'u yok. Kabuk komutu yok; paket sorgusu sabit mutlak yoldur.
UI, paket listesi/URL/ham ortam değişkenlerini rapora dahil etmez.
Rapor yalnız uygulama/sürüm/aile, masaüstü/oturum türü ve sayısal
kaynak değerlerini içerir. CPU modeli, kullanıcı, hostname, IP/MAC,
seri numarası, süreç adı, ev dizini ve pano içeriği dışarı aktarılmaz.
URL alanı parola içerebilir; hiçbir günlük veya kalıcı kayıt tutulmaz.

## Paket ve destek

Debian kaynak paketi: debhelper 13, dh-python, pybuild/setuptools;
Architecture: all; python3 >=3.9, python3-gi, gir1.2-gtk-3.0.
Saf Python olması ARM'da test edildiği anlamına gelmez; öncelik amd64.
Geliştirici bilgisayarı macOS olduğundan portable .deb üretimi ayrıca
sağlanır; resmî yayın paketi Linux'ta dpkg-buildpackage ile üretilir.

Otomatik test: Debian11/12/13 ortak tabanları VE resmî
pardus/yirmibir,yirmiuc,yirmibes imajları. Bunlar gerçek oturum testi değildir.
Yayın kapısı: 21/23/25 × XFCE/GNOME amd64 VM; uygun oturumlarda X11/Wayland.
21 EOL olduğundan yalnız uygulama geriye uyumluluğu hedeflenir.
OS güvenlik desteği iddiası yok; resmî takvim çelişkisi docs/COMPATIBILITY.md'de.

## Kabul ölçütleri

Çekirdek testleri Python3.9'da geçer; bozuk/eksik veri çökertmez;
modül kapatma işini durdurur; dosyalar 0600; rapor izin verilen alanlarla
sınırlıdır; .deb kurulup açılır ve kaldırılır; kapalı inhibitör/eksik D-Bus
başarı diye gösterilmez. Gerçek VM kanıtı yoksa sürüm yalnız önizlemedir.
