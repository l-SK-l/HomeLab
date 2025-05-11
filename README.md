# HomeLab
Hello, everyone! This is my little home lab. This is a temporary host for my educational purposes, when I have more space I will buy more serious hardware))) and this host will become a firewall.

![Host](Docs/Img/XCY_X30.png)

## Server Specs
| KEY | VALUE |
|--------|:-----------:|
| Model | XCY X30|
| CPU | Intel N100 |
| Storage 1 | 256GB |
| Storage 2 | 1TB |
| RAM | 16GB |
| Net Iface | x4 2.5Gbe |

## Running systems
- [Proxmox](https://www.proxmox.com/en/)
- [Duplicati](https://www.duplicati.com/)
- [Grafana](https://grafana.com/)
- [Pi-hole](https://pi-hole.net/)
- [Nginx Proxy Manager](https://nginxproxymanager.com/)
- [Portainer.io](https://www.portainer.io/)
- [InfluxDB](https://www.influxdata.com/)
- [Prometheus](https://prometheus.io/)
- [It-tools](https://github.com/CorentinTh/it-tools)
- [Stirling PDF](https://github.com/Stirling-Tools/Stirling-PDF)
- [Uptime-kuma](https://github.com/louislam/uptime-kuma)
- [Speedtest Tracker](https://github.com/alexjustesen/speedtest-tracker)
- [Heimdall](https://github.com/linuxserver/Heimdall)
- [Scrutiny](https://github.com/AnalogJ/scrutiny)
- [n8n](https://n8n.io/)
- [Semaphore](https://semaphoreui.com/)
- [qBittorrent](https://www.qbittorrent.org/)
- [Paperless-ngx](https://docs.paperless-ngx.com/)

## Grafana
[![grafana](Docs/Img/grafana.gif)]()
### Dashboards
Check [Grafana folder](grafana/) It syncs automatically.

## Backups
Local backup jobs by schedule for VM/Containers and work laptope then encrypted backups using [Duplicati](https://www.duplicati.com/) to Google Disk

## Heimdall
[![Heimdall](Docs/Img/Heimdall.png)]()

## Semaphore(Ansible)
* [Debian update --limit debian](ansible/upd_debian.yml)
* [VPNs update --limit vpn](ansible/upd_debian.yml)
* [Update Docker --limit docker](ansible\upd_docker_containers.yml)
* [Clean unused Docker images --limit docker](ansible\clean_unused_docker_images.yml)
* [PVE update --limit vpe](ansible/upd_debian.yml)
* [Update Pi-hole --limit pihole](ansible\upd_pihole.yml)

## Scrutiny
[![Scrutiny](Docs/Img/Scrutiny.png)]()

## Public domains
[Cloudflare tunnel](https://www.cloudflare.com/products/tunnel/) + [Nginx Proxy Manager](https://nginxproxymanager.com/) provides easy access to the homelab from the internet with HTTPS and strict allow policies + [Crowdsec](https://www.crowdsec.net/) as alternative fail2ban
