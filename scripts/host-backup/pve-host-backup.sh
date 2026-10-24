#!/bin/bash
# Proxmox host configuration backup -> /mnt/pve/ssd/dump/host-backup
# Duplicati picks this folder up together with VM/LXC backups and uploads it (encrypted) to Google Drive.
# Install: /usr/local/sbin/pve-host-backup.sh (chmod 700) + cron file from this folder.
set -uo pipefail
umask 077
DEST=/mnt/pve/ssd/dump/host-backup
KEEP=2
TS=$(date +%F_%H%M)
OUT="$DEST/pve-host-$TS.tar.zst"

mountpoint -q /mnt/pve/ssd || { echo "ERROR: /mnt/pve/ssd is not mounted"; exit 1; }
if pgrep -x vzdump >/dev/null; then echo "ERROR: vzdump is running, skipping"; exit 1; fi
mkdir -p "$DEST"
WORK=$(mktemp -d "$DEST/.tmp-XXXX")
trap 'rm -rf "$WORK"' EXIT
M="$WORK/meta"; mkdir -p "$M"

# /etc/pve is copied as plain files (tar below). Do NOT touch the live config.db with sqlite3:
# an external sqlite client removes the WAL of the running pmxcfs.

# Reference info for recovery
pveversion -v            > "$M/pveversion.txt"
dpkg --get-selections    > "$M/dpkg-selections.txt"
apt-mark showmanual      > "$M/apt-manual.txt"
lsblk -f                 > "$M/lsblk.txt"
blkid                    > "$M/blkid.txt"
{ pvs; vgs; lvs; }       > "$M/lvm.txt" 2>&1
{ ip -br a; ip r; }      > "$M/network.txt"
cat /proc/cmdline        > "$M/cmdline.txt"
crontab -l               > "$M/root-crontab.txt" 2>/dev/null
systemctl list-unit-files --state=enabled > "$M/enabled-units.txt"

tar --zstd -cpf "$OUT.part" --warning=no-file-changed \
  --exclude='etc/pve/.*' --exclude='root/.cache' --exclude='root/*.deb' \
  --exclude='root/cloudflared-*.bak' \
  -C "$WORK" meta \
  -C / etc root opt usr/local var/spool/cron
rc=$?
if [ $rc -gt 1 ]; then echo "ERROR: tar rc=$rc"; rm -f "$OUT.part"; exit 1; fi
mv "$OUT.part" "$OUT"

# Keep only the last KEEP archives locally (older versions are kept by Duplicati)
ls -1t "$DEST"/pve-host-*.tar.zst | tail -n +$((KEEP+1)) | xargs -r rm -f
echo "OK: $OUT ($(du -h "$OUT" | cut -f1))"
