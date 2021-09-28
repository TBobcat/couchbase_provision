#!/bin/bash 
# run script as a sudoer
# script assumes there's only one backup in the gs bucket and restores from it

set -e

export PATH=/opt/couchbase/bin:$PATH
mkdir /data/backup_migrate

# config backup folder and bakup repo for couchbase
cbbackupmgr config -a /data/backup_migrate -r cluster --disable-data

gsutil cp -m -r gs://cb_backup/cluster/* /data/backup_migrate/cluster/

cbbackupmgr restore -a /data/backup_migrate  -r cluster -c http://127.0.0.1:8091 \
    -u Administrator -p password  --auto-create-buckets