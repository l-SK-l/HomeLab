# How to set up a new LXC

## Change root password
```sh
passwd root
```

## Open SSH for root
```sh
sed -i 's/#\?PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config && systemctl restart ssh
```

## Add to automation
- Add the container to the Semaphore inventory (group `debian`, plus `docker` / `pihole` if relevant) so it gets automatic updates — see [Ansible](../ansible/README.md).
- Docker hosts: connect them to Dockhand (via the Hawser agent) for container management and updates.

## Monitoring
Nothing to install — the container appears in Grafana Cloud automatically through pve-exporter. See [Monitoring](Monitoring.md).
For a web service, add a check in Uptime Kuma.

## Publishing a service
If the service should be reachable from the internet: add a proxy host in Nginx Proxy Manager (traffic comes only through the Cloudflare tunnel) and a local DNS record in Pi-hole.

## Backups
Add the container to the vzdump backup job in Proxmox (unless it is deliberately excluded).
