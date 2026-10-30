# Katkı

Python3.9 sözdizimi sınırını koruyun. Sistem GTK3'ü ve standart kütüphaneyi
tercih edin; sırf gelecekte gerekecek diye katman/bağımlılık eklemeyin.
Yeni araç sabit modül listesine ve izin açıklamasına eklenir; dışarıdan
Python eklentisi yüklenmez. Her modül kapanırken işini bırakmalıdır.

İnternet istemcisi, analitik, reklam, hata yükleme, otomatik güncelleme,
kullanıcı hesabı ve e-posta girişi bu ürünün kapsamı dışındadır. Ağ
gerektiren katkılar kabul edilmemelidir. Lisans/varlık kaynağı belirtin;
referans uygulamadan kod veya tasarım kopyalamayın. Sentetik test verisi
kullanın; kullanıcı raporu, URL veya envanterini repoya eklemeyin.

`python3 -m unittest discover -s tests -v` temel kontroldür; GTK değişikliği
Linux Xvfb testi ve etkilenen Pardus oturum VM kontrolünü de gerektirir.
PR'de ne değiştiği, neden ve gerçek test sonucu yazılmalıdır. Yeni veri
kalıcılığı/IPC eklenirse iki dildeki bildirim ve güvenlik sınırı yeniden
incelenir. Ağsız tasarım kararı korunur.
