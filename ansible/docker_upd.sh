#!/bin/bash

# Set -e to exit immediately if a command exits with a non-zero status.
set -e

# Get variables from environment (Ansible's --extra-vars)
REMOTE_HOSTS=${REMOTE_HOSTS}
REMOTE_USER=${REMOTE_USER:-root}
SSH_PASSWORD=${SSH_PASSWORD}

# Check if REMOTE_HOSTS is set
if [ -z "$REMOTE_HOSTS" ]; then
  echo "Error: REMOTE_HOSTS is not set."
  echo "Usage: REMOTE_HOSTS=<host1,host2,...> REMOTE_USER=<user> SSH_PASSWORD=<password> ./docker_upd.sh"
  exit 1
fi

# Split the comma-separated hosts into an array
IFS=',' read -r -a HOSTS <<< "$REMOTE_HOSTS"

# Loop through each host
for REMOTE_HOST in "${HOSTS[@]}"; do
  echo "Starting Watchtower on $REMOTE_HOST..."

  # Use sshpass for password-based authentication (less secure, but works without PTY)
  # Alternatively, use SSH keys (more secure)
  sshpass -p "$SSH_PASSWORD" ssh -o StrictHostKeyChecking=no $REMOTE_USER@$REMOTE_HOST "docker run -v /var/run/docker.sock:/var/run/docker.sock --rm containrrr/watchtower --run-once"

  # Check the exit code of the ssh command
  if [ $? -ne 0 ]; then
    echo "Error: Failed to run Watchtower on $REMOTE_HOST"
    exit 1
  fi

  echo "Watchtower completed on $REMOTE_HOST"
done

echo "Watchtower execution completed on all hosts."
