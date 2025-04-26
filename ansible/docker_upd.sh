#!/bin/bash

REMOTE_HOSTS=$1
REMOTE_USER=${2:-root}
SSH_PASSWORD=$3

if [ -z "$REMOTE_HOSTS" ]; then
  echo "Error: The list of hosts is not specified."
  echo "Running: $0 <host1,host2,...> [user] [password]"
  exit 1
fi

IFS=',' read -r -a HOSTS <<< "$REMOTE_HOSTS"

for REMOTE_HOST in "${HOSTS[@]}"; do
  echo "Starting Watchtower on $REMOTE_HOST..."

  expect -c "
    set timeout 30
    spawn ssh $REMOTE_USER@$REMOTE_HOST \"docker run -v /var/run/docker.sock:/var/run/docker.sock --rm containrrr/watchtower --run-once\"
    expect {
      \"*assword:\" {
        send \"$SSH_PASSWORD\\r\"
        exp_continue
      }
      \"*yes/no*\" {
        send \"yes\\r\"
        exp_continue
      }
      eof
    }
  "

  if [ $? -ne 0 ]; then
    echo "Error: The command could not be executed on the host $REMOTE_HOST"
  fi
done

echo "Watchtower execution completed on all hosts."