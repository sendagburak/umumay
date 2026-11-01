# Uyumluluk — güncel hedef ve tarihî test kanıtları

0.1.4 bir paketleme düzeltmesidir; hedef aileler değişmedi. Güncel sürümün
sonucu [GitHub Actions](https://github.com/sendagburak/umumay/actions)
kaydından, tarihî 0.1.3 sonucu aşağıdaki sabit koşudan izlenir.

31 Ekim 2026: Umumay **0.1.3**, Pardus 21/23/25 ve Debian 11/12/13
kullanıcı alanlarındaki altı GitHub CI görevini başarıyla tamamladı.
[Doğrulanmış koşu ve paket commit'i](https://github.com/sendagburak/umumay/actions/runs/41141196995).
Her aile kendi native paketini üretip kurdu, GTK/Xvfb akışını çalıştırdı
ve paketi kaldırdı. Pardus görevleri gerçek GNOME/XFCE idle API'lerini de
sınadı. Yayımlanan .deb, bu koşunun Pardus 25.2 çıktısıdır; eşleşen tam
kaynak aynı sürümde sunulur. Tam ISO/Wayland/donanım sınırları aşağıda kalır.

Aşağıdaki eski yerel test sütunu yalnız **0.1.1** kanıtıdır ve yeni
sürümün sonucuyla birleştirilmez. Ayrıntı: [güncel doğrulama](VALIDATION.md).

| Pardus ailesi | Debian tabanı | Beklenen Python | GTK ortak taban | 0.1.1 yerel test |
| --- | --- | --- | --- | --- |
| 25 Bilge (25.2) | 13 Trixie | 3.13 | 3.24 | Paket/GTK + GNOME/XFCE API geçti |
| 23 Ay Yıldız (23.5) | 12 Bookworm | 3.11 | 3.24 | Paket/GTK + GNOME/XFCE API geçti |
| 21 Dolunay (21.5) | 11 Bullseye | 3.9 | 3.24 | Paket/GTK + GNOME/XFCE API geçti; EOL |

Kaynaklar: [Pardus indirme](https://pardus.org.tr/surumler/),
[yaşam döngüsü](https://pardus.github.io/lifecycle/),
[25 paketleri](https://indir.pardus.org.tr/ISO/Pardus25/Pardus-25.0-GNOME-amd64.packages),
[23 paketleri](https://indir.pardus.org.tr/ISO/Pardus23/Pardus-23.0-GNOME-amd64.packages).
Pardus21 resmî kullanıcı alanında Python3.9.2/GTK3.24.24 doğrudan çalıştırıldı.
İlk tasarımda kullanılan Debian taban kaynakları: [Python](https://packages.debian.org/bullseye/python3),
[GTK](https://packages.debian.org/bullseye/gir1.2-gtk-3.0).

Resmî destek sayfalarında fark var: [ana takvim](https://pardus.org.tr/pardus-surum-yonetimi/)
21 için 2025-05-01, 23 için 2027 Q3, 25 için 2029 H2 belirtirken yaşam
döngüsü sayfası güvenlik desteği sonlarını 21 için 2026-08-31, 23 için
2028-06-30, 25 için 2030-06-30 veriyor. Bu tarihlerden biri kesinmiş gibi
kullanılmamalı. İkisine göre de 21 bugün destek dışıdır. Uygulama geriye
uyumluluğu işletim sistemine güvenlik desteği sağlamaz.

CI altı tabanı ayrı test eder: debian:bullseye/bookworm/trixie ve Pardus
resmî hesabındaki pardus/yirmibir,yirmiuc,yirmibes. İmaj içinde ID ve
VERSION_ID beklenen aileyle eşleşmelidir. EOL imaj veya depo erişimi
bozulursa test başarısız olmalı; Debian testi Pardus testi diye sunulmamalı.

Tarihî 0.1.1 yerel oturumunda çalışanlar üç gerçek Pardus OCI kullanıcı alanıdır; Linux
çekirdeği Lima/Debian ARM64 VM'sine aittir ve amd64 süreçler Rosetta ile
çalışmıştır. GTK, Xvfb/X11'de sınandı. Uyanık tutma testleri UID1000 ile
gerçek GNOME SessionManager ve XFCE servislerini ayrı özel D-Bus üzerinde
kullandı. Bu, tam GNOME Shell/XFCE ISO kurulumu veya Wayland testi değildir.
21/23'te eski XFCE PowerManager API'si, 25'te XFCE ScreenSaver API'si
doğrulandı. O yerel kayıt sırasında GitHub işleri henüz çalıştırılmamıştı.
Güncel 0.1.3 GitHub sonuçları üstte ayrı verilmiştir.

## Gerçek VM yayın kapısı (tamamı bekliyor)

| Ortam (amd64) | Aç/kapat, kur/kaldır | Yerel araçlar/modül tercihleri | Idle süre/iptal | Ağ izi, gizlilik, klavye |
| --- | --- | --- | --- | --- |
| 21 XFCE / X11 | Bekliyor | Bekliyor | Bekliyor | Bekliyor |
| 21 GNOME / mevcut X11-Wayland | Bekliyor | Bekliyor | Bekliyor | Bekliyor |
| 23 XFCE / X11 | Bekliyor | Bekliyor | Bekliyor | Bekliyor |
| 23 GNOME / mevcut X11-Wayland | Bekliyor | Bekliyor | Bekliyor | Bekliyor |
| 25 XFCE / mevcut X11-Wayland | Bekliyor | Bekliyor | Bekliyor | Bekliyor |
| 25 GNOME / mevcut X11-Wayland | Bekliyor | Bekliyor | Bekliyor | Bekliyor |

Her VM'de ISO hash'i, imaj digest'i (varsa), Python/GTK ve D-Bus servis
adları kayıt altına alınmalı; kullanıcı kimliği/hostname kaydedilmemeli.
Paket Architecture: all'dur; ARM desteği test edilmiş değildir.
