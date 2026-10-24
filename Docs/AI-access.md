# AI access to the homelab

The homelab can be operated by an AI assistant (Claude) — for diagnostics, routine maintenance and documentation.
The goal is "full control with protection": the assistant can do almost everything, but destructive actions need a human.

## How it works

- **[ProxmoxMCP-Plus](https://github.com/RekklesNA/ProxmoxMCP-Plus)** — an MCP server that gives the assistant access to the Proxmox API (nodes, VMs, LXCs, storage, backups, snapshots). It runs on the workstation, not on the server.
- Access uses a dedicated Proxmox **API token**, not the root password.
- Commands on the host and inside containers are allowed, but filtered by a **deny list** (reboot/shutdown, destroying VMs/CTs, wiping disks, etc.).
- **Destructive operations** (delete, rollback, restore) require a one-time confirmation code from me for every single operation.
- **SSH** from the workstation is kept as a fallback channel.
- Access is only possible from the home LAN — Proxmox is not exposed to the AI from the internet.

## Rules for the assistant

- Read first, change second; show what will change before doing it.
- Ask before touching backups (Duplicati) and anything holding important data.
- Everything learned or changed goes into docs, not just chat history.
