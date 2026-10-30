# Logo ve masaüstü kimliği / Logo and desktop identity

Özgün yükselen kuş simgesi, kullanıcının isteğiyle bu proje için yapay zekâ
ile üretildi. Başka bir projenin varlığı alınmadı. Ana PNG
`umumay/umumay.png` içindedir. `data/icons/` standart simge boyutlarını
içerir. Aynı görsel proje lisansı GPL-3.0-or-later ile dağıtılır. Bu bir
marka tescili veya üçüncü kişilerin haklarına karşı güvence değildir.

The original raised-wing bird was generated for this project at the user's
request. The master PNG and standard-size exports are included under
GPL-3.0-or-later. This does not claim trademark registration or exclusivity.

Application/desktop ID: `io.github.sendagburak.umumay`.
Icon name: `umumay`. Binary package and command: `umumay`.

GTK penceresi ve uygulama başlığı dosyayı yerelden yükler. Kurulum,
freedesktop hicolor tema dizinlerine PNG'leri ve uygulama menüsüne desktop
dosyasını koyar. Ayatana AppIndicator desteklenirse yerel gösterge kullanılır.
Yoksa GTK'nin X11 StatusIcon geri dönüşü vardır. Görünür bir alan sağlamak
masaüstünün sorumluluğudur. GNOME'da ilgili eklentiler gerekebilir.

Resmî teknik açıklamalar: [GTK StatusIcon](https://docs.gtk.org/gtk3/class.StatusIcon.html),
[GNOME AppIndicator desteği](https://extensions.gnome.org/extension/615/appindicator-support/).
Kaynak kurulum için kısayol düğmesi önce `umumay` komutunun kurulu
olmasını ister. Kısayol seçilen yerde 0700 izinle oluşturulur. Mevcut dosya
ve sembolik bağlantıların üzerine yazılmaz. Oturum, dosyayı güvenilir
başlatıcı olarak ayrıca onaylamanı isteyebilir.

Top-edge notch artwork is a concept only. No notch panel is implemented.
