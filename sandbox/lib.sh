#!/bin/sh

USERNAME=$(whoami)

if [ $USERNAME = "jovyan" ]; then
    pip install --no-deps -r $(dirname $0)/config/requirements.txt
    pip install --no-deps -r $(dirname $0)/config/sandbox_reqs.txt
else
    echo "Run in jupyter server"
    echo $USERNAME
fi
