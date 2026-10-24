# Scripts

Scripts and configs that live on the Proxmox host. Copies here are the reference versions — secrets are replaced with placeholders.

| Path | Installed to | Purpose |
|---|---|---|
| [host-backup/pve-host-backup.sh](host-backup/pve-host-backup.sh) | `/usr/local/sbin/` | Weekly archive of the host configuration (`/etc`, `/etc/pve`, `/root`, `/opt`, `/usr/local`, cron) plus recovery info (package list, disks, LVM, network). Keeps the 2 latest archives next to VM backups, so Duplicati ships them off-site too |
| [host-backup/pve-host-backup.cron](host-backup/pve-host-backup.cron) | `/etc/cron.d/pve-host-backup` | Schedule: runs when no vzdump jobs are active |
| [alloy/config.alloy](alloy/config.alloy) | `/etc/alloy/config.alloy` | Grafana Alloy: host metrics, Proxmox API metrics via pve-exporter, journald logs → Grafana Cloud. See [Monitoring](../Docs/Monitoring.md) |
| [hookscripts/htpc-vt-switch.sh](hookscripts/htpc-vt-switch.sh) | `/var/lib/vz/snippets/` | LXC hookscript: switches the host console to VT7 after a container that drives the HDMI output starts |
