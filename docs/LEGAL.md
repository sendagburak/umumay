# Hukuki risk azaltma ve yayın sınırı

Bu belge hukuki uygunluk garantisi veya kişiye özel hukuk görüşü değildir.
Önlemler somut davranışa dayanır: hesap/ödeme/pazarlama/hosting/yükleme
hizmeti, telemetri ve internet aktarımı eklenmedi. Kullanıcı yalnız yerel
araçları çalıştırır. Yayımlanan kodu indirme ve geliştiricinin GitHub'da
iletişim kurması ayrıca değerlendirilir; uygulama bunları otomatik yapmaz.

## KVKK

Türkçe/İngilizce bildirimler `umumay/privacy_*.txt` içinde ve
uygulamanın ilk ekranındadır. Aynı dosyalar paketlenir; farklı bir web
metniyle çelişki üretilmez. Yerel ölçüm ve kullanıcı girdisi işlenir;
"hiçbir veri işlenmez" veya "KVKK hiçbir koşulda uygulanmaz" denmez.

KVKK açıklamaları veri sorumlusu kimliği, amaç, alıcılar, toplama
yöntemi/hukuki sebep ve m.11 haklarının gerçek faaliyetle açıklanmasını
gerektirir. Kimlik veya hukuki sebep uydurulmadı. Yayıncı/kurumsal kullanım
bağlama göre ayrıca belirleneceğinden metin bir belirli veri sorumlusu için tamamlanmış
m.10 uygunluk belgesi olarak sunulmaz. Uygulama onay/e-posta toplamaz.
Yurt dışına aktarım yapılmadığı tasarımı, sonradan eklenecek bir API için
izin veya hukuki dayanak oluşturmaz. Böyle bir özellik bu ürün kapsamında
eklenmemelidir.

Resmî dayanaklar, 30 Ekim 2026'da kontrol edildi:
[KVKK aydınlatma açıklaması](https://www.kvkk.gov.tr/Icerik/2033/Aydinlatma-Yukumlulugu-),
[aydınlatma tebliği](https://www.kvkk.gov.tr/Icerik/4132/aydinlatma-yukumlulugunun-yerine-getirilmesinde-uyulacak-usul-ve-esaslar-hakkinda-teblig),
[güncel yurt dışı aktarım açıklaması](https://www.kvkk.gov.tr/Icerik/2053/Yurtdisina-Aktarim).
Eski aktarım rejimine ait sayfalardan güncel hüküm çıkarılmadı; ceza
tutarları üzerinden bir uygunluk hesabı yapılmadı.

## Fikrî haklar ve GPL

Vorssaint'in yalnız kamusal özellik/lisans/marka/gizlilik açıklamaları
referans alındı. Swift kaynak kodu, görsel yerleşim, logo, ikon, metin ve
özel API alınmadı. Referans depodaki standart GNU GPL v3 lisans metni
lisans belgesi olarak kullanıldı; uygulama kodu taşınmadı. Bizim
GPL-3.0-or-later seçimi bağımsız karardır. Yeni kuş logosu bu proje için
yapay zekâ ile üretilmiş PNG'dir ve aynı lisansla sunulur. Kullanıcının seçtiği ürün adı **Umumay**'dır;
resmî Pardus/TÜBİTAK/ULAKBİM ürünü veya onaylı proje olduğu iddia edilmez.
Pardus adı yalnız uyumluluk açıklamalarında kullanılır, ürün adının parçası
değildir. Resmî Pardus logosu kullanılmaz. Umumay için sınırlı kelime sorgusu
bir marka izni/tescil kararı değildir; benzerlik ve diğer haklar ayrıca
incelenmelidir. İsim hikâyesi ve araştırma sınırı docs/NAME.md içindedir.
GTK/PyGObject dağıtımın paketlerinden kullanılır; ikili kopyaları bu
pakete gömülmez. Python standart kütüphanesi ve sistem araçları kullanılır.
Paketle tam karşılık gelen kaynak, build dosyaları, lisans ve telif
bildirimleri birlikte dağıtılmalıdır. [GNU resmî GPL açıklaması](https://www.gnu.org/licenses/gpl-faq.en.html)

## Genel yayın öncesi gerekli kararlar

1. Seçilen Umumay adı, app ID, gerçek yayıncı ve güvenlik/iletişim kanalı;
   marka taraması yapılmadan adın hukuken temiz olduğu söylenemez.
2. Yayıncı kimliğiyle mevcut bilgi metninin son kontrolü; kurumsal kullanım
   veya ayrı destek sürecinde yeni veri akışı varsa ayrıca değerlendirme.
3. Yeni Umumay paket adıyla Linux GTK, kurulum ve standart Debian build;
   ayrıca tam ISO/Wayland/donanım kanıtı. 0.1.1 testleri yeni ikilinin
   tamamlanmış doğrulaması olarak gösterilmemeli.
4. Public issue'larda kişisel veri/rapor istememe; gerçek güvenlik kanalı.
5. İmzalı yayınlar, doğrulanmış maintainer alanları, karşılık gelen kaynak.

Güncel kaynak/paket dağıtımı GitHub sendagburak/umumay kanalındadır.
Bakımcı alanında GitHub hesabının noreply adresi kullanılır; uygulama
e-posta göndermez. Bu hesap tanımı bir şirket/veri sorumlusu kimliği
veya marka tescili olduğu anlamına gelmez.
