# Umumay mimarisi / Architecture

Umumay, Python 3.9+ ve sistem GTK3 ile çalışan yerel bir Linux masaüstü uygulamasıdır.
Hesap, sunucu, web API'si, SDK veya API anahtarı gerektirmez.

| Parça | Görevi |
| --- | --- |
| core.py | /proc ve /etc/os-release okuma, sayısal ölçümler ve salt okunur dpkg-query |
| storage.py | Sabit modül tercihleri ve açık kullanıcı seçimiyle sınırlı JSON raporu |
| links.py | Elle girilen bağlantı metnini açmadan ve DNS sorgusu yapmadan ayrıştırma |
| awake.py / desktop.py | Süreli uyanık tutma ve yerel oturum D-Bus hizmetleri |
| branding.py / tray.py | Paketlenmiş logo, açık seçilen kısayol ve yerel bildirim alanı |
| ui.py | Tek GTK penceresi, hızlı araçlar ana sayfası, araç ekranları, isteğe bağlı gizlilik metinleri ve gecikmeli paket araması |

D-Bus çağrıları bilgisayardaki GNOME/XFCE hizmetlerine gider; internet API'si değildir.
Kullanıcı girdileri GTK'de düz metin olarak gösterilir. Paket sorgusu sabit
komut ve argümanlarla, kabuk olmadan, süre sınırıyla çalışır.

Otomatik kalıcılık kapalı modül kimlikleriyle sınırlıdır. URL ve paket listesi
geçmişi tutulmaz. Rapor ve masaüstü kısayolu için açık kullanıcı eylemi gerekir.
Ayrıntılar: [gizlilik](PRIVACY.md), [güvenlik sınırı](SECURITY.md).

The installed application has no web backend, network client, API credentials,
analytics or updater. System and session interfaces are local. CI image preparation
and GitHub distribution are developer services, separate from application runtime.

Geliştirme becerileri, ajan yönergeleri ve oturum notları uygulamanın bağımlılığı
değildir. Kaynak arşivi yalnız tanımlanmış proje dizinlerinden üretilir.
