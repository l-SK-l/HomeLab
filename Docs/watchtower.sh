#!/bin/sh

REMOTE_HOST="docker.elfacloud.com"
REMOTE_USER="USER"

ssh $REMOTE_USER@$REMOTE_HOST "docker run -v /var/run/docker.sock:/var/run/docker.sock --rm containrrr/watchtower --run-once"