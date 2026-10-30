# Güvenlik ve izin sınırı

Normal kullanıcı. Root yardımcı, sudo çağrısı, setuid, daemon, otomatik
başlangıç ve polkit politikası yoktur. Kurulumdaki apt yetkisiyle programın
çalışma zamanı yetkisi ayrıdır. Kabuk çalıştırılmaz; tek dış program
`/usr/bin/dpkg-query` sabit argümanlarla, 10 saniye sınırıyla çalışır.
Paket/URL metinleri GTK'de düz metindir; HTML/markup çalıştırılmaz.

İnternet istemcisi ve uzak kaynak yoktur. `runtime.py` TCP ekran/D-Bus
adreslerini reddeder; `desktop.py` yalnız yerel Unix oturum bus'ını kullanır.
Uygulamanın açık D-Bus arayüzleri, sabit idle hizmeti çağrıları ve yerel
bildirim alanı bütünleşmesidir. GTK/Gio'nun kendi yerel IPC'si sistem
bağımlılığıdır. Veri başka bir uygulamaya URL veya rapor olarak yollanmaz.
Uyanık tutma otomatik kilidi geciktirebilir; kullanıcıya açıklanır. Süre
sonunda, modül kapanışında ve uygulama kapanışında istek bırakılır. Özel
bağlantının kapanması da inhibitörün yaşam süresini sonlandırır.

Tercihler atomik ve 0600; yeni uygulama tercih dizini 0700'dür. Doğrudan
dosya/üst dizin symlink'leri reddedilir. Aynı kullanıcı hesabını ele geçiren
bir program karşısında izolasyon garantisi değildir. Raporlar sınırlı alan
listesinden üretilir. Ağ diskleri/bulut senkronizasyonu işletim sistemi
seviyesinde ayrıca engellenmelidir.

Testler statik ağ istemcisi taraması, Python socket/DNS kapatma ve CI'da
`--network none` Docker çalışmasını içerir. Önceki 0.1.1 sürümü üç resmî Pardus kullanıcı
alanında gerçek GTK akışlarında strace ile sınandı; AF_INET/AF_INET6 hedefli
bağlantı görülmedi. Testlerin paket indirme hazırlığı ayrıdır. Tam ISO
oturumu, fiziksel güç yönetimi ve Wayland için VM checklist ayrıca gerekir.
Güncel sürümün gerçek CI sonuçları ve sınırı docs/VALIDATION.md içindedir.
Kaynağın ağ kodu içermemesi gelecekteki bağımlılık değişikliklerinin de
denetlenmesi gereğini ortadan kaldırmaz.

## Bildirim

GitHub private vulnerability reporting kanalı kök SECURITY.md dosyasında
verilmiştir. Herhangi bir gerçek kullanıcı bilgisi, URL, paket
envanteri veya sistem raporu public issue'ya yapıştırılmamalıdır. Geliştirme
örnekleri sentetik olmalıdır. Destek süresi şu an yalnız 0.1.x önizlemedir.
