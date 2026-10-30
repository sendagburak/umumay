> Tarihî kapsam: Aşağıdaki başarı gözlemleri 0.1.1 sürümüne aittir.
> Umumay 0.1.2 Linux GTK/paket testi henüz tekrarlanmadı; docs/VALIDATION.md.

# Test kapsamı

F01 gerçek /proc CPU/RAM/disk, ilk/ikinci örnek, yerel rapor ve 0600;
F02 gerçek dpkg ve arama; F03 cookie, süre sonu ve gerçek GNOME/XFCE API;
F04 Unicode/imzalı/hatalı URL ve GTK; F05 bozuk/symlink ayar ve switch
rollback: üç Pardus ailesinde geçti. Dört gerçek ekran görüntüsü alındı.

Standart Debian build, aynı .deb'nin üç ailede kur/çalıştır/kaldırılması,
ağsız GTK strace izi, VS Code Dev Containers ve normal kullanıcı testleri
çalıştırıldı. Linux'ta 31/31. Ayrıntılar docs/VALIDATION.md'dedir.

Tam ISO masaüstü, Wayland, fiziksel ekran/kapak/suspend, GPU, klavye ve
ekran okuyucuyla insan kullanılabilirliği denetimi ayrıca bekliyor.
