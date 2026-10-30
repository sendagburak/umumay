# Gizlilik / Privacy

Tek kaynaklı, uygulamanın da yerelden gösterdiği metinler:

- [Türkçe aydınlatma ve yerel işleme bildirimi](../umumay/privacy_tr.txt)
- [English privacy and local processing notice](../umumay/privacy_en.txt)

`ui.py` metinleri paketten okur; web sayfası veya haricî içerik açmaz.
Paket kurulumu/indirme, kurulu uygulamanın çalışma zamanı değildir.

| Veri | Amaç / yer | Saklama | Alıcı |
| --- | --- | --- | --- |
| CPU/RAM/disk, uptime, aile/oturum türü | Seçili ekranda gösterim / RAM | Kapanışa kadar | Yok |
| Paket adı ve sürümü | Yerel arama / RAM | Kapanışa kadar; modül kapatılınca liste temizlenir | Yok |
| Elle girilen URL | Yerel ayrıştırma / RAM | Kapanışa veya modül kapanışına kadar | Yok |
| Kapalı sabit modül kimlikleri | $XDG_CONFIG_HOME/umumay/settings.json veya ~/.config/umumay/settings.json | Kullanıcı silene kadar | Yok |
| Sınırlı rapor | Kullanıcı seçtiğinde dosyaya | Kullanıcı silene kadar | Yok |
| Sabit masaüstü başlatıcısı | Kullanıcı seçtiğinde dosyaya, 0700 | Kullanıcı silene kadar | Yok |

Yerel işleme ile geliştiricinin veri toplaması aynı şey değildir; "hiçbir
veri işlenmez" iddiası kullanılmaz. GUI'de Araçları aç seçilmeden
ölçüm/paket sorgusu başlatılmaz. Belgelenen CLI --report komutu, kullanıcının
açık isteğiyle GUI göstermeden rapor üretir. Otomatik günlük ve hata yükleyici yoktur.
İşletim sisteminin kendi günlükleri, swap ve bulut/yedekleme araçları bu
programın kontrolünde değildir. Kullanıcı bunları da ayrı yönetmelidir.
