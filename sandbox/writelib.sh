#!/bin/sh

USERNAME=$(whoami)

if [ $USERNAME = "jovyan" ]; then
    pip list --format=freeze > $(dirname $0)/config/sandbox_reqs.txt
else
    echo "Run in jupyter server"
    echo $USERNAME
fi
