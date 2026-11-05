# SPDX-License-Identifier: GPL-3.0-or-later
"""Single native GTK window, fixed modules, no online resources."""

import threading
import shutil
from pathlib import Path

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GdkPixbuf, Gio, GLib, Gtk

from .awake import AwakeController
from .autostart import AutostartError, is_autostart_enabled, set_autostart
from .branding import APP_ID, ICON_FILE, create_shortcut
from .core import collect_snapshot, installed_packages
from .desktop import IdleBackend
from .links import clean_url
from .notch import NotchShell
from .storage import MODULES, SettingsStore, StorageError, write_report
from .tray import StatusArea


def label(text=''):
    widget = Gtk.Label(label=text, xalign=0)
    widget.set_line_wrap(True)
    widget.set_selectable(True)
    return widget


def button(box, text, callback):
    widget = Gtk.Button(label=text)
    widget.connect('clicked', callback)
    box.pack_start(widget, False, False, 0)
    return widget


def size_text(value):
    return '—' if value is None else '%.1f GiB' % (value / 1024 ** 3)


class UtilityApp(Gtk.Application):
    def __init__(self):
        GLib.set_prgname(APP_ID)
        GLib.set_application_name('Umumay')
        super().__init__(application_id=APP_ID, flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.store = SettingsStore()
        self.disabled, self.settings_error = set(), ''
        try:
            self.disabled = self.store.load()
        except StorageError as error:
            self.settings_error = str(error)
        self.awake = AwakeController(IdleBackend())
        self.started = True
        self.closed = False
        self.generation = 0
        self.package_loading = False
        self.last_cpu = None
        self.snapshot = None
        self.window = None
        self.notch = None
        self.tray = None
        self._hide_notice_sent = False

    def do_activate(self):
        if self.window is not None:
            self._show_notch()
            return
        Gtk.Settings.get_default().set_property('gtk-recent-files-enabled', False)
        self.window = Gtk.ApplicationWindow(application=self, title='Umumay · Önizleme')
        self.window.set_wmclass('umumay', APP_ID)
        Gtk.Window.set_default_icon_from_file(str(ICON_FILE))
        self.window.set_icon_from_file(str(ICON_FILE))
        self.window.connect('destroy', self._close)
        self.window.connect('delete-event', self._hide_to_tray)
        # Closing is always the same safe action as the panel's close button.
        # A true quit is reserved for the notification-area menu.
        action = Gio.SimpleAction.new('hide', None)
        action.connect('activate', self._hide_to_tray)
        self.add_action(action)
        self.set_accels_for_action('app.hide', ['<Primary>q'])
        root = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        root.set_border_width(12)
        self.stack = Gtk.Stack()
        sidebar = Gtk.StackSidebar(stack=self.stack)
        root.pack_start(sidebar, False, False, 0)
        root.pack_start(self.stack, True, True, 0)
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        heading = Gtk.Box(spacing=10, margin=12)
        self.brand_image = Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_scale(
            str(ICON_FILE), 48, 48, True))
        self.brand_image.get_accessible().set_name('Umumay logosu')
        heading.pack_start(self.brand_image, False, False, 0)
        heading.pack_start(label('Umumay · Yerel masaüstü araçları'), True, True, 0)
        close_button = Gtk.Button(label='×  Kapat')
        close_button.set_tooltip_text('Bildirim alanına gizle; oradaki menüden tamamen çıkabilirsiniz')
        close_button.connect('clicked', self._hide_to_tray)
        heading.pack_end(close_button, False, False, 0)
        content.pack_start(heading, False, False, 0)
        content.pack_start(root, True, True, 0)
        self.notch = NotchShell(self.window, content, ICON_FILE)
        self._privacy_page()
        self._system_page()
        self._packages_page()
        self._awake_page()
        self._links_page()
        self._settings_page()
        self.stack.connect('notify::visible-child-name', self._page_changed)
        self.window.show_all()
        self._apply_disabled()
        self.stack.set_visible_child_name('system')
        self.notch.after_show()
        self.tray = StatusArea(self.window, on_show=self._show_notch, on_quit=self._really_quit)
        GLib.timeout_add_seconds(2, self._tick)

    def _show_notch(self, *_):
        if self.window is None or self.closed:
            return
        self.window.show()
        self.notch.expand(pin=True)
        self.window.present()
        self._tick()

    def _hide_to_tray(self, *_):
        if self.closed or self.window is None:
            return False
        if self.tray is None or not self.tray.can_background():
            warning = Gtk.MessageDialog(
                transient_for=self.window, modal=True,
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.OK,
                text='Bildirim alanı bulunamadı')
            warning.format_secondary_text(
                'Umumay görünmeden arka planda kalmayacak. XFCE bildirim alanını '
                'etkinleştirin veya Umumay’ı açık bırakın.')
            warning.run()
            warning.destroy()
            return True
        self.notch.state.escape()
        self.notch._apply_view()
        self.window.hide()
        if not self._hide_notice_sent:
            notification = Gio.Notification.new('Umumay arka planda çalışıyor')
            notification.set_body(
                'Bildirim alanındaki Umumay simgesinden çentiği yeniden açın '
                'veya “Tamamen çık” seçeneğini kullanın.')
            self.send_notification('umumay-background', notification)
            self._hide_notice_sent = True
        return True

    def _really_quit(self, *_):
        if self.window is not None and not self.closed:
            self.window.destroy()
        self.quit()

    def _page(self, name, title):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(box)
        self.stack.add_titled(scroll, name, title)
        return box

    def _privacy_page(self):
        box = self._page('privacy', 'Gizlilik / Privacy')
        box.pack_start(label('Umumay · Bağımsız proje; resmî Pardus ürünü değildir.\nHesap yok. Telemetri yok. Sunucu bağlantısı yok.\nIndependent project. No account, telemetry or server connection.'), False, False, 0)
        language = Gtk.ComboBoxText()
        language.append('tr', 'Türkçe')
        language.append('en', 'English')
        language.set_active_id('tr')
        box.pack_start(language, False, False, 0)
        view = Gtk.TextView(editable=False, cursor_visible=False, wrap_mode=Gtk.WrapMode.WORD)
        box.pack_start(view, True, True, 0)
        def show_notice(combo):
            path = Path(__file__).with_name('privacy_%s.txt' % combo.get_active_id())
            try:
                text = path.read_text(encoding='utf-8')
            except OSError:
                text = 'Gizlilik belgesi yüklenemedi. / Privacy notice could not be loaded.'
            view.get_buffer().set_text(text)
        language.connect('changed', show_notice)
        show_notice(language)
        button(box, 'Araçları aç / Open tools', self._enter)

    def _enter(self, *_):
        self.started = True
        first = next((m.id for m in MODULES if m.id not in self.disabled), 'settings')
        self.stack.set_visible_child_name(first)
        self._tick()

    def _system_page(self):
        box = self._page('system', 'Sistem')
        self.system_info = label('Araçları açtığınızda yerel ölçümler gösterilir.')
        box.pack_start(self.system_info, False, False, 0)
        self.bars = {}
        for name in ['CPU', 'Bellek', 'Disk /']:
            bar = Gtk.ProgressBar(show_text=True, text=name)
            box.pack_start(bar, False, False, 0)
            self.bars[name] = bar
        box.pack_start(label('Rapor: yalnız aile, oturum türü ve sayısal kaynak değerleri. Kullanıcı adı, IP, paket listesi ve URL içermez. Yerel dosya yöneticisinde ağ/eşitlenen konum seçmeyin.'), False, False, 0)
        button(box, 'Raporu yerel dosyaya kaydet…', self._export)
        self.export_status = label()
        box.pack_start(self.export_status, False, False, 0)

    def _packages_page(self):
        box = self._page('packages', 'Paketler')
        box.pack_start(label('Yalnız kurulu Debian paketleri; yükleme, kaldırma veya çevrimiçi arama yapılmaz.'), False, False, 0)
        self.search = Gtk.SearchEntry(placeholder_text='Paket adı veya sürüm ara')
        self.search.get_accessible().set_name('Kurulu paketlerde ara')
        box.pack_start(self.search, False, False, 0)
        self.package_status = label('Liste henüz okunmadı.')
        box.pack_start(self.package_status, False, False, 0)
        self.package_list = Gtk.ListStore(str, str)
        filtered = self.package_list.filter_new()
        filtered.set_visible_func(lambda model, row, _: self.search.get_text().casefold() in
                                  (model[row][0] + ' ' + model[row][1]).casefold(), None)
        self.search.connect('search-changed', lambda *_: filtered.refilter())
        tree = Gtk.TreeView(model=filtered)
        for index, title in enumerate(['Paket', 'Sürüm']):
            tree.append_column(Gtk.TreeViewColumn(title, Gtk.CellRendererText(), text=index))
        box.pack_start(tree, True, True, 0)
        button(box, 'Listeyi yenile', lambda *_: self._load_packages())

    def _awake_page(self):
        box = self._page('awake', 'Uyanık tut')
        box.pack_start(label('Oturuma göre ekranın boşta kalmasını veya otomatik güç tasarrufunu erteler; otomatik kilidi geciktirebilir. Elle kilitleme ve kapak davranışını değiştirmez. Pencere kapanınca bırakılır.'), False, False, 0)
        self.duration = Gtk.ComboBoxText()
        for minutes in [15, 30, 60, 120]:
            self.duration.append(str(minutes), '%d dakika' % minutes)
        self.duration.set_active(0)
        box.pack_start(self.duration, False, False, 0)
        button(box, 'Başlat', self._start_awake)
        button(box, 'Durdur', self._stop_awake)
        self.awake_status = label('Pasif; hiçbir ayar değiştirilmedi.')
        box.pack_start(self.awake_status, False, False, 0)

    def _links_page(self):
        box = self._page('links', 'Bağlantı')
        box.pack_start(label('URL’yi elle yapıştırın. Adres açılmaz; DNS sorgusu yapılmaz; pano izlenmez. Bilinen imzalı bağlantılar değiştirilmez.'), False, False, 0)
        self.url_input = Gtk.Entry(placeholder_text='https://…', max_length=8192)
        self.url_input.get_accessible().set_name('Temizlenecek bağlantı')
        box.pack_start(self.url_input, False, False, 0)
        button(box, 'Takip parametrelerini temizle', self._clean_link)
        self.url_output = Gtk.Entry(editable=False)
        self.url_output.get_accessible().set_name('Temizlenmiş bağlantı')
        box.pack_start(self.url_output, False, False, 0)
        self.url_status = label()
        box.pack_start(self.url_status, False, False, 0)

    def _clean_link(self, *_):
        try:
            self.url_output.set_text(clean_url(self.url_input.get_text()))
            self.url_status.set_text('İşlem yerelde tamamlandı. Sonucu seçerek kopyalayabilirsiniz.')
        except ValueError as error:
            self.url_output.set_text('')
            self.url_status.set_text(str(error))

    def _settings_page(self):
        box = self._page('settings', 'Modüller')
        self.settings_status = label(self.settings_error or 'Tercihler yalnız bu bilgisayara kaydedilir.')
        box.pack_start(self.settings_status, False, False, 0)
        button(box, 'Masaüstü kısayolu oluştur…', self._desktop_shortcut)
        self.autostart_toggle = Gtk.CheckButton(
            label='Oturum açıldığında Umumay çentiğini otomatik başlat')
        self.autostart_toggle.set_active(is_autostart_enabled())
        self.autostart_toggle.connect('toggled', self._toggle_autostart)
        box.pack_start(self.autostart_toggle, False, False, 0)
        box.pack_start(label(
            'İsteğe bağlıdır. Oturum açıldığında çentik kapalı hâlde üst ortada görünür; '
            'üzerine geldiğinizde genişler. “Kapat” çentiği bildirim alanına gizler, '
            'bildirim alanındaki “Tamamen çık” uygulamayı sonlandırır.'
        ), False, False, 0)
        self.switches = {}
        for module in MODULES:
            toggle = Gtk.CheckButton(label=module.title + ' — ' + module.description)
            toggle.set_active(module.id not in self.disabled)
            toggle.connect('toggled', self._toggle, module.id)
            self.switches[module.id] = toggle
            box.pack_start(toggle, False, False, 0)

    def _toggle_autostart(self, toggle):
        try:
            enabled = set_autostart(toggle.get_active())
        except AutostartError as error:
            self.settings_status.set_text(str(error))
            toggle.handler_block_by_func(self._toggle_autostart)
            toggle.set_active(is_autostart_enabled())
            toggle.handler_unblock_by_func(self._toggle_autostart)
        else:
            self.settings_status.set_text(
                'Oturum açıldığında başlatma etkin.' if enabled
                else 'Oturum açıldığında başlatma devre dışı.')

    def _desktop_shortcut(self, *_):
        if shutil.which('umumay') is None:
            self.settings_status.set_text('Kısayolu kullanmak için önce .deb paketini kurun.')
            return
        dialog = Gtk.FileChooserDialog(title='Umumay masaüstü kısayolu', transient_for=self.window,
                                       action=Gtk.FileChooserAction.SAVE)
        dialog.add_buttons('Vazgeç', Gtk.ResponseType.CANCEL, 'Oluştur', Gtk.ResponseType.OK)
        dialog.set_local_only(True)
        desktop = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DESKTOP)
        if desktop:
            dialog.set_current_folder(desktop)
        dialog.set_current_name('Umumay.desktop')
        try:
            if dialog.run() == Gtk.ResponseType.OK:
                try:
                    create_shortcut(Path(dialog.get_filename()))
                    self.settings_status.set_text('Kısayol oluşturuldu. Gerekirse dosyaya sağ tıklayıp başlatmaya izin verin.')
                except OSError:
                    self.settings_status.set_text('Kısayol oluşturulamadı; mevcut dosyalar değiştirilmez.')
        finally:
            dialog.destroy()

    def _toggle(self, toggle, module_id):
        disabled = set(self.disabled)
        disabled.discard(module_id) if toggle.get_active() else disabled.add(module_id)
        try:
            if module_id == 'awake' and module_id in disabled:
                self.awake.stop()
            self.store.save(disabled)
        except (RuntimeError, StorageError) as error:
            self.settings_status.set_text(str(error))
            toggle.handler_block_by_func(self._toggle)
            toggle.set_active(module_id not in self.disabled)
            toggle.handler_unblock_by_func(self._toggle)
            return
        self.disabled = disabled
        if 'packages' in disabled:
            self.generation += 1  # in-flight read has a 10s ceiling; its result is discarded
            self.package_list.clear()
        if 'links' in disabled:
            self.url_input.set_text('')
            self.url_output.set_text('')
        if 'system' in disabled:
            self.snapshot, self.last_cpu = None, None
        self._apply_disabled()
        self.settings_status.set_text('Yerel tercihler kaydedildi.')

    def _apply_disabled(self):
        for module in MODULES:
            self.stack.get_child_by_name(module.id).set_visible(module.id not in self.disabled)

    def _page_changed(self, *_):
        name = self.stack.get_visible_child_name()
        if not self.started and name not in {'privacy', 'settings'}:
            self.stack.set_visible_child_name('privacy')
            return
        if name == 'packages' and 'packages' not in self.disabled:
            self._load_packages()

    def _load_packages(self):
        if not self.started or 'packages' in self.disabled or self.closed or self.package_loading:
            return
        self.package_loading = True
        self.generation += 1
        generation = self.generation
        self.package_status.set_text('Yerel liste okunuyor…')
        def worker():
            try:
                rows, message = installed_packages(), ''
            except RuntimeError as error:
                rows, message = [], str(error)
            GLib.idle_add(self._packages_ready, generation, rows, message)
        threading.Thread(target=worker, daemon=True).start()

    def _packages_ready(self, generation, rows, message):
        self.package_loading = False
        if self.closed or 'packages' in self.disabled:
            return False
        if generation != self.generation:
            if self.stack.get_visible_child_name() == 'packages':
                self._load_packages()
            return False
        self.package_list.clear()
        for row in rows:
            self.package_list.append([row.name, row.version])
        self.package_status.set_text(message or '%d kurulu paket. Arama yalnız bu listededir.' % len(rows))
        return False

    def _start_awake(self, *_):
        try:
            self.awake.start(int(self.duration.get_active_id()))
            self.awake_status.set_text('Etkin; %d dakika kaldı.' % (self.awake.remaining // 60 + 1))
        except (RuntimeError, GLib.Error) as error:
            self.awake_status.set_text(str(error))

    def _stop_awake(self, *_):
        try:
            self.awake.stop()
            self.awake_status.set_text('Pasif; istek bırakıldı.')
        except RuntimeError as error:
            self.awake_status.set_text(str(error))

    def _tick(self):
        if self.closed:
            return False
        if self.started and self.stack.get_visible_child_name() == 'system' and 'system' not in self.disabled:
            self.snapshot = collect_snapshot(self.last_cpu)
            self.last_cpu = self.snapshot.cpu
            s = self.snapshot
            family = 'Pardus %s' % s.release.family if s.release.family else 'Hedef Pardus ailesi doğrulanamadı'
            warning = '\nPardus 21 dağıtım desteği dışında; uygulama uyumluluğu OS güvenlik desteği değildir.' if s.release.family == 21 else ''
            self.system_info.set_text('%s · %s / %s\nÇalışma süresi: %s dakika%s' %
                                      (family, s.desktop, s.session, s.uptime_seconds // 60 if s.uptime_seconds is not None else '—', warning))
            values = {'CPU': (s.cpu_percent, 'CPU: %s' % ('%.1f%%' % s.cpu_percent if s.cpu_percent is not None else 'ilk örnek/veri yok')),
                      'Bellek': (100 * s.memory.used / s.memory.total if s.memory else None,
                                 'Bellek: %s / %s' % (size_text(s.memory.used if s.memory else None), size_text(s.memory.total if s.memory else None))),
                      'Disk /': (100 * s.disk_used / s.disk_total if s.disk_total else None,
                                 'Disk /: %s / %s' % (size_text(s.disk_used), size_text(s.disk_total)))}
            for name, (percent, text) in values.items():
                self.bars[name].set_fraction(max(0, min(1, (percent or 0) / 100)))
                self.bars[name].set_text(text)
        if self.awake.active:
            try:
                self.awake.tick()
                self.awake_status.set_text('Etkin; %d saniye kaldı.' % self.awake.remaining if self.awake.active else 'Süre doldu; istek bırakıldı.')
            except RuntimeError as error:
                self.awake_status.set_text(str(error))
        return True

    def _export(self, *_):
        if self.snapshot is None:
            self.export_status.set_text('Önce Sistem sayfasında yerel bir ölçüm alın.')
            return
        dialog = Gtk.FileChooserDialog(title='Yerel JSON raporu', transient_for=self.window,
                                       action=Gtk.FileChooserAction.SAVE)
        dialog.add_buttons('Vazgeç', Gtk.ResponseType.CANCEL, 'Kaydet', Gtk.ResponseType.OK)
        dialog.set_local_only(True)
        dialog.set_do_overwrite_confirmation(True)
        dialog.set_current_name('sistem-raporu.json')
        try:
            if dialog.run() == Gtk.ResponseType.OK:
                try:
                    write_report(Path(dialog.get_filename()), self.snapshot)
                    self.export_status.set_text('Yerel dosya kaydedildi; hiçbir yere gönderilmedi.')
                except StorageError as error:
                    self.export_status.set_text(str(error))
        finally:
            dialog.destroy()

    def _close(self, *_):
        if self.closed:
            return
        self.closed = True
        if self.notch is not None:
            self.notch.close()
            self.notch = None
        self.generation += 1
        if self.tray is not None:
            self.tray.close()
            self.tray = None
        try:
            self.awake.stop()
        except RuntimeError:
            pass
        self.awake.backend.close()
