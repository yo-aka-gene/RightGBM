#!/bin/sh

VMNAME = $((basename $PWD) | tr '[A-Z]' '[a-z]')-jupyterlab-1

docker exec $VMNAME python -m pip install -r $(basename $0)/config/requirements.txt
docker exec $VMNAME python -m pip install -r $(basename $0)/config/sandbox_reqs.txt
