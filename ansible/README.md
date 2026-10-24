# Ansible

Playbooks are run from [Semaphore UI](https://semaphoreui.com/) on a schedule.
Inventory and secrets (Key Store) live in Semaphore, playbooks come from this repository.

## Playbooks

| Playbook | Semaphore task (`--limit`) | What it does |
|---|---|---|
| [upd_debian.yml](upd_debian.yml) | `debian`, `vpn`, `pve` | `apt update` + `dist-upgrade`, autoremove/autoclean, reports hosts that need a reboot |
| [upd_pihole.yml](upd_pihole.yml) | `pihole` | `pihole -up` |
| [test_connection.yml](test_connection.yml) | `debian` | Connectivity / facts check |

Docker containers are **no longer** updated by Ansible — updates are handled in Dockhand (web UI for Docker hosts).
The old Docker playbooks are kept in [archive/](archive/) for reference only, their Semaphore tasks are disabled.

## ansible.cfg
```ini
[defaults]
interpreter_python = auto_silent
library         = ~/library/:/usr/share/ansible/library/
module_utils    = ~/library/utils/:/usr/share/ansible/library/utils/
host_key_checking = False
stdout_callback = community.general.yaml
callbacks_enabled = webhook, community.general.yaml
deprecation_warnings = False

[callback_webhook]
url = http://<n8n-host>:5678/webhook/<webhook-id>
http_method = POST
headers = {"Content-Type": "application/json"}
body_format = json
timeout = 10

[persistent_connection]
connect_timeout = 30
connect_retries = 30
connect_interval = 1
```

## Custom webhook callback plugin
[webhook.py](webhook.py) sends a short run summary (playbook, status, duration, per-host stats) to n8n, which forwards notifications.

Install: copy `ansible/webhook.py` to `/usr/share/ansible/plugins/callback_plugins/webhook.py` (requires the `requests` Python library).
