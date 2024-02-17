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
- [ChatGPT-Next-Web](https://github.com/ChatGPTNextWeb/ChatGPT-Next-Web)
- [Uptime-kuma](https://github.com/louislam/uptime-kuma)
- [Cronicle](https://github.com/jhuckaby/Cronicle)
- [Speedtest Tracker](https://github.com/alexjustesen/speedtest-tracker)

## Grafana
[![grafana](Docs/Img/grafana.gif)]()
### Dashboards
* [Node Exporter Full](https://grafana.com/grafana/dashboards/1860) For VMs and LXC containers
* [Proxmox Cluster [Flux]](https://grafana.com/grafana/dashboards/15356) For Proxmox
* [Monitor PI-HOLE ](https://grafana.com/grafana/dashboards/19760-monitor-pi-hole-sparta) For Pi-Hole

## Backups
Local backup jobs by schedule + [Duplicati](https://www.duplicati.com/) encrypted backups to Google Drive

## Public domains
[Cloudflare tunnel](https://www.cloudflare.com/products/tunnel/) + [Nginx Proxy Manager](https://nginxproxymanager.com/) provides easy access to the homelab from the internet with HTTPS and strict allow policys

## Promts for Chat GPT
[Masks for NextChat](Docs/ai-masks.json)