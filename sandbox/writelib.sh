#!/bin/sh

VMNAME = $((basename $PWD) | tr '[A-Z]' '[a-z]')-jupyterlab-1

docker exec -it $VMNAME sudo pip list --format=freeze > $(basename $0)/config/sandbox_reqs.txt
