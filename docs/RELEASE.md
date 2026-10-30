# Yayın ve dağıtım / Releases

Kaynak deposu: https://github.com/sendagburak/umumay

İlk yayın 0.1.3 geliştirme önizlemesidir. GitHub sürümü **pre-release**
olarak işaretlenir. Türkçe README, İngilizce README.en.md, GPL tam metni,
iki dilde gizlilik bildirimi, logo ve paketleme kaynakta birlikte tutulur.
Yayımlanan ikiliyle tam karşılık gelen kaynak arşivi ve SHA256 sağlanır.

Linux paketi `dpkg-buildpackage -us -uc -b` ile oluşturulur. CI'da kurulur,
gerçek GTK/Xvfb akışı çalıştırılır ve kaldırılır. Geliştirici Mac'inde
`tools/build_preview.py` ayrıca taşınabilir önizleme üretebilir. Bu çıktı
standart Debian build ve Linux çalışma kanıtı olarak adlandırılmaz.

Release assets must identify whether the .deb came from native Linux CI
or the portable preview builder. Keep the exact matching source available
at the same time and record SHA256 values. A checksum is not a publisher
signature. No signing key was invented or generated in the user's name.

Önizleme imzasızdır. Kararlı sürüm öncesinde yayıncı anahtarı, imzalı etiket
ve paket doğrulaması, korunan ana dal, dağıtım imajlarının digest'e
sabitlenmesi ve tam ISO/XFCE/GNOME/Wayland/donanım kontrolleri tamamlanmalıdır.
Mevcut CI action'ları commit'e sabitlidir. Dağıtım imajları etiket kullanır.

Uygulamaya güncelleme sorgusu eklenmez. Güncelleme kullanıcının paket
yöneticisiyle veya yeni sürümü elle indirmesiyle yapılır. Çevrimdışı
kurulum için bağımlılıklar önceden temin edilir. Kaldırma, kullanıcının
tercih, rapor veya kısayol dosyalarını kendiliğinden silmez.

Repository descriptions and release notes are written in Turkish and
English using Kalemdar's natural-writing and multilingual guidance.
Do not publish local workstation paths, audit working files, personal
information or old screenshots under the new version's name.
