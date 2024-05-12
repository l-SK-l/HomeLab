## Change root password
```sh
passwd root
```

## Open ssh for root
```sh
sed -i 's/#\?PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config && sudo service ssh restart
```

## Set up Prometheus job
Fetch and unpack the latest release from the releases page and create a symlink so that /opt/node_exporter refers to the current version.

```sh
cd /root
wget https://github.com/prometheus/node_exporter/releases/download/v1.8.0/node_exporter-1.8.0.linux-amd64.tar.gz
tar -C /opt -xvzf node_exporter-1.8.0.linux-amd64.tar.gz 
```

Create the logical link to the current node_exporter version:
```sh
ln -s node_exporter-X.Y.Z.linux-amd64 /opt/node_exporter
```
The logical link allows us to create systemd unit file without needing to update it each time we upgrade node_exporter.

Create a systemd unit file 
```sh
nano /etc/systemd/system/node_exporter.service
```
```sh
[Unit]
Description=Prometheus Node Exporter
Documentation=https://github.com/prometheus/node_exporter
After=network-online.target

[Service]
User=root
EnvironmentFile=/etc/default/node_exporter
ExecStart=/opt/node_exporter/node_exporter $OPTIONS
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Tell systemd to read this new file:
```sh
systemctl daemon-reload
```
Create an options file 
```sh
sh -c 'echo "OPTIONS=''" > /etc/default/node_exporter'
```

Let’s start node_exporter:
```sh
systemctl enable node_exporter
systemctl start node_exporter
systemctl status node_exporter
```

Add new job to Prometheus
```sh
nano /etc/prometheus/prometheus.yml
```

Restart Prometheus
```sh
systemctl restart prometheus
```
