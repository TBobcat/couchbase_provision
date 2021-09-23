#!/bin/bash 
# run script as a sudoer
export PATH=/opt/couchbase/bin:$PATH
mkdir /data/backup

# config backup folder and bakup repo for couchbase
cbbackupmgr config -a /data/backup -r cluster --disable-data

gsutil cp -r gs://cb_backup/cluster/* /data/backup/cluster/

cbbackupmgr restore -a /data/backup  -r cluster -c http://127.0.0.1:8091 \
    -u Administrator -p password --force-updates --auto-create-buckets