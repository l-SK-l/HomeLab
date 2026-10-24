#!/bin/bash
# Proxmox LXC hookscript: switch the host console to VT7 after the container starts.
# Used for a container that runs Xorg directly on the host's HDMI output.
# Install: /var/lib/vz/snippets/htpc-vt-switch.sh (storage "local" must allow content "snippets"),
#          pct set <CTID> --hookscript local:snippets/htpc-vt-switch.sh
CTID="$1"
PHASE="$2"
if [ "$PHASE" == "post-start" ]; then
    chvt 7 || true
fi
exit 0
