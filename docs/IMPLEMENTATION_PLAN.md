# İlk sürüm uygulama planı

Amaç: özgün, yerel Pardus masaüstü araçları önizlemesi.
Kaynak mimari: ../replica/architecture.md. Ürün adı: Umumay.

1. Çekirdek: önce fixtures ile CPU/RAM/os-release/kurulu paket ayrıştırma,
   eksik veri, CPU sayaç gerilemesi ve resmi aile sınırları testleri.
   `Snapshot` immutable veri; `collect_snapshot(previous_cpu=None)`;
   `installed_packages()` timeout'lu salt okunur sorgu.
2. Yerel veri: `SettingsStore(path).load/save`; sabit MODULES kataloğu;
   bilinmeyen kimlik reddi; bozuk JSON, symlink, 0600/atomik yazma testleri.
   `write_report(path, snapshot)` izinli alanlardan yeni rapor üretir.
3. Araçlar: `clean_url(text)` yalnız http(s), izleme anahtarları listesi,
   yinelenen parametreler, imzalı URL, Unicode/boş/güvensiz şema testleri.
   `AwakeController(backend, clock)`: start(minutes), stop(), tick();
   fake backend ile hata, süre sonu ve çift başlatma testleri.
4. GTK: sabit beş sayfa; paket sorgusu worker; modül kapanışı/oturum
   yokluğu/rapor kaydı hatası; Linux Xvfb smoke testi gerçek GTK ile.
5. Paket: Debian kaynak dizini, portable önizleme .deb, masaüstü girişi,
   özgün ikon; paket içeriği ve tekrarlanabilir üretim kontrolü.
6. CI ve belge: altı container hedefi; altı gerçek masaüstü VM yayın kapısı;
   GPL tam metni, katkı/güvenlik/gizlilik ve GitHub yayın adımları.

Doğrulama: `python3 -m unittest discover -s tests -v`, `compileall`,
portable build ve bağımsız `ar`/`tar` kontrolü. CI ve gerçek VM testleri
burada çalıştırılamazsa sonuçlar açıkça bekliyor olarak kalır.
