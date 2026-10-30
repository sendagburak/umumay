# SPDX-License-Identifier: GPL-3.0-or-later
"""URL parsing only; never resolves or opens a host."""

from urllib.parse import unquote_plus, urlsplit, urlunsplit

TRACKERS = frozenset({'fbclid', 'gclid', 'dclid', 'msclkid', 'mc_cid', 'mc_eid', '_hsenc', '_hsmi'})
SIGNATURES = frozenset({'signature', 'sig', 'x-amz-signature', 'x-goog-signature'})


def clean_url(text):
    if not isinstance(text, str) or len(text) > 8192 or any(ord(c) < 32 for c in text):
        raise ValueError('Bağlantı geçersiz veya çok uzun.')
    text = text.strip()
    try:
        parsed = urlsplit(text)
        if parsed.scheme.lower() not in {'http', 'https'} or not parsed.hostname:
            raise ValueError('Yalnız geçerli HTTP/HTTPS bağlantıları kullanılabilir.')
        if parsed.username is not None or parsed.password is not None:
            raise ValueError('Kullanıcı adı/parola içeren bağlantı kullanmayın.')
        if any(c.isspace() for c in text):
            raise ValueError('Bağlantı içinde boşluk olmamalı.')
        _ = parsed.port  # validate malformed/out-of-range ports, without I/O
        fields = parsed.query.split('&') if parsed.query else []
        keys = [unquote_plus(field.partition('=')[0]).lower() for field in fields]
        if SIGNATURES.intersection(keys):
            return text
        kept = [field for field, key in zip(fields, keys) if key not in TRACKERS and not key.startswith('utm_')]
        return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, '&'.join(kept), parsed.fragment))
    except (ValueError, UnicodeError) as error:
        raise ValueError(str(error)) from error
