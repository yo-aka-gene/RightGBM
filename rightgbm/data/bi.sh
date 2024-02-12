#!/bin/sh

DATANAME="bi"
DATA_URL=$1
META_URL=$2

mkdir $(dirname $0)/$DATANAME
curl -o $(dirname $0)/$DATANAME/$DATANAME.tar $1
tar -xvf $(dirname $0)/$DATANAME/$DATANAME.tar -C $(dirname $0)/$DATANAME
gzip -d $(dirname $0)/$DATANAME/*.gz
curl -o $(dirname $0)/$DATANAME/$DATANAME.xlsx $2
