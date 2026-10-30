#!/bin/sh
set -eu
mkdir -p /run/dbus /tmp/umumay-runtime
chown 1000:1000 /tmp/umumay-runtime
chmod 700 /tmp/umumay-runtime
dbus-daemon --system --fork --nopidfile
exec runuser -u umumaytest -- env HOME=/home/umumaytest XDG_RUNTIME_DIR=/tmp/umumay-runtime \
  dbus-run-session -- xvfb-run -a sh /src/tools/session-test.sh "$1"
