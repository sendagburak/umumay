<p align="center"><img src="data/icons/128x128/apps/umumay.png" width="96" height="96" alt="Umumay bird logo"></p>

# Umumay

**Runs on your computer. Keeps your information with you.**

Small, modular desktop tools for Pardus and Debian. Check system resources,
search installed packages, keep your screen awake for a limited time and
remove tracking parameters from links. No account, email address or server
connection is required.

[Türkçe](README.md) · [Downloads](https://github.com/sendagburak/umumay/releases)
· [Privacy](docs/PRIVACY.md) · [GPL-3.0-or-later](LICENSE)

Umumay is an independent open-source project, not an official Pardus or
TÜBİTAK/ULAKBİM product. **0.1.4 is a development preview.** It targets
Pardus 25, 23 and 21 with Python 3.9+ and GTK 3.24. Pardus 21 is outside
distribution support; application compatibility does not extend OS security support.

## Tools

| Tool | Function |
| --- | --- |
| System | Current CPU, memory, root disk usage and uptime |
| Packages | Read-only search through locally installed Debian packages |
| Keep Awake | A 15–120 minute idle/power-saving inhibitor when supported by the session |
| Link | Local tracking-parameter removal from a manually entered URL |
| Modules | Enable or disable tools and explicitly create a desktop shortcut |

The bird logo is bundled for the application header, window, launcher,
taskbar and supported notification areas. Create a shortcut through
**Modüller → Masaüstü kısayolu oluştur…**. Your file manager may require
you to allow launching it. GNOME needs desktop support for AppIndicators
and desktop file icons. Umumay does not install or enable extensions.
Closing the window exits the application and releases its idle inhibitor.

The development source adds a home screen with direct tool shortcuts,
optional access to the privacy notice and a manual copy action for cleaned
links. The top-edge notch panel is still a design concept, not yet implemented.
The interface is Turkish; the bundled privacy notice is available in Turkish
and English. These changes are not included in the published 0.1.4 package.

## Install

Download the matching `.deb`, source archive and `SHA256SUMS` from
[Releases](https://github.com/sendagburak/umumay/releases).

```sh
sha256sum -c SHA256SUMS
sudo apt install ./umumay_0.1.4_all.deb
umumay
```

`apt` may download missing dependencies. Prepare them beforehand for an
offline installation. This preview is unsigned. Checksums verify content
integrity, not publisher identity.

To run from the source directory:

```sh
sudo apt install python3 python3-gi gir1.2-gtk-3.0 gir1.2-ayatanaappindicator3-0.1
python3 -m umumay
```

Ayatana integration is optional, with a legacy X11 tray fallback. Without
a compatible tray host the tools remain usable in the application window.

## Local processing

Metrics, package inventories and entered links are processed in memory.
Links are never visited or resolved, and the clipboard is not monitored.
Only disabled module IDs are saved automatically. Reports and desktop
shortcuts require an explicit save action. Avoid network mounts and
cloud-synchronised folders. OS-level synchronisation is outside the app's control.

There are no payments, subscriptions, analytics, telemetry, crash uploads,
ads or automatic update checks. GitHub downloads, dependency installation
and development CI are separate from installed-app runtime.

[English notice](umumay/privacy_en.txt) · [Türkçe bildirim](umumay/privacy_tr.txt)

## Development

```sh
python3 -m unittest discover -s tests -v
RUN_GTK_TESTS=1 dbus-run-session -- xvfb-run -a python3 -m unittest discover -s tests -v
dpkg-buildpackage -us -uc -b
```

CI covers Debian 11/12/13 and official Pardus 21/23/25 userlands, with
networking disabled in test containers. This is not full Pardus ISO,
GNOME Shell, Wayland or physical hardware validation.
[Validation scope](docs/VALIDATION.md) distinguishes current results from historical tests.

[Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) ·
[Architecture](docs/ARCHITECTURE.md) · [Brand assets](docs/BRANDING.md)

The original name is inspired by the Hüma bird, without claiming to be
a historical variant. No Vorssaint code, logo or design was copied.
The source and bundled logo are provided under GPL-3.0-or-later.
