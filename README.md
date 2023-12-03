# HomeLab

## Ansible
Update Debian hosts:
```sh
ansible-playbook -i hosts upd_debian.yml
```
Install prometheus_node_exporter and alert_manager for new host:
```sh
ansible-playbook -i hosts /etc/ansible/grafana_stack/install_monitoring.yml
```

## Grafana
### Dashboards
* [Node Exporter Full](https://grafana.com/grafana/dashboards/1860) For VMs and LXC containers
* [Proxmox Cluster [Flux]](https://grafana.com/grafana/dashboards/15356) For Proxmox

## Backups
Local backup jobs by schedule + [Duplicati](https://www.duplicati.com/) encrypted backups to Google Drive (temporarily)