#!/bin/sh

VMNAME=$((basename $PWD) | tr '[A-Z]' '[a-z]')-jupyterlab-1

sh auth.sh docker-compose.yml
docker compose up -d
docker start $VMNAME
open http://localhost:8008
