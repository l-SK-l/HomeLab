## I use ansible via Semaphore UI
Inventory and Key Store into Semaphore UI

Playbooks from these repository

## ansible.cfg
[defaults]
interpreter_python = auto_silent
library         = ~/library/:/usr/share/ansible/library/
module_utils    = ~/library/utils/:/usr/share/ansible/library/utils/
host_key_checking = False
stdout_callback = community.general.yaml
callbacks_enabled = webhook, community.general.yaml
deprecation_warnings = False

[callback_webhook]
url = http://n8nhostname:5678/webhook/e5fba21d-da05-47d7-922f-6f99e0f6b777
http_method = POST
headers = {"Content-Type": "application/json"}
body_format = json
timeout = 10

[persistent_connection]
connect_timeout = 30
connect_retries = 30
connect_interval = 1

## Custom Webhook plagin
ansible\webhook.py into /usr/share/ansible/plugins/callback_plugins/webhook.py
