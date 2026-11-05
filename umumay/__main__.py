# SPDX-License-Identifier: GPL-3.0-or-later
import argparse
import os
import sys
from pathlib import Path

from . import __version__
from .core import collect_snapshot
from .runtime import validate_local_session
from .notch import require_x11_notch
from .storage import write_report


def main():
    parser = argparse.ArgumentParser(description='Umumay — yerel masaüstü sistem araçları.')
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--report', type=Path, metavar='DOSYA', help='Sınırlı yerel JSON raporu kaydet; hiçbir yere göndermez.')
    args = parser.parse_args()
    try:
        if args.report:
            write_report(args.report, collect_snapshot())
            print('Yerel rapor kaydedildi.')
            return 0
        validate_local_session()
        require_x11_notch(os.environ.get('DISPLAY', ''))
        # Keep GTK's file/settings integration local and avoid persistent chooser preferences.
        os.environ.update(GIO_USE_VFS='local', GSETTINGS_BACKEND='memory', GTK_USE_PORTAL='0')
        from .ui import UtilityApp
        return UtilityApp().run([sys.argv[0]])
    except (RuntimeError, ImportError) as error:
        if isinstance(error, ImportError):
            print('GTK bağımlılıkları gerekli: python3-gi ve gir1.2-gtk-3.0.', file=sys.stderr)
        else:
            print(str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
