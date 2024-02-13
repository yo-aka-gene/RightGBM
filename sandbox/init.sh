#!/bin/sh

VMNAME=$((basename $PWD) | tr '[A-Z]' '[a-z]')-jupyterlab-1

sh auth.sh docker-compose.yml
docker compose up -d
docker start $VMNAME
docker exec $VMNAME sudo pip -U pip
sh $(dirname $0)/lib.sh
sh $(dirname $0)/writelib.sh
open http://localhost:8008
