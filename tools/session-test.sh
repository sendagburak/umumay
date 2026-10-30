#!/bin/sh
set -eu
mkdir -p "$XDG_RUNTIME_DIR"
chmod 700 "$XDG_RUNTIME_DIR"
xfwm4 > /tmp/wm.log 2>&1 &
wm_pid=$!
case "$1" in
  xfce)
    if command -v xfce4-screensaver >/dev/null; then
      xfce4-screensaver > /tmp/session.log 2>&1 &
    else
      xfce4-power-manager --no-daemon > /tmp/session.log 2>&1 &
    fi ;;
  gnome)
    session_binary=/usr/libexec/gnome-session-binary
    [ -x "$session_binary" ] || session_binary=/usr/lib/gnome-session/gnome-session-binary
    "$session_binary" --session=umumay-test --disable-acceleration-check > /tmp/session.log 2>&1 & ;;
  *) exit 2 ;;
esac
session_pid=$!
trap 'kill "$session_pid" "$wm_pid" 2>/dev/null || true' EXIT
if ! PYTHONPATH=/src python3 /src/tools/session_check.py "$1"; then
    cat /tmp/session.log
    exit 1
fi
