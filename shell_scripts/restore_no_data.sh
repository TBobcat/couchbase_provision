#!/bin/bash 
# run script as a sudoer
# script assumes there's only one backup in the gs bucket and restores from it
# script nees cred.sh sourced to get credentials from exported environment variable

set -e

export PATH=/opt/couchbase/bin:$PATH

rm -rf /data/backup_migrate
mkdir /data/backup_migrate

# config backup folder and bakup repo for couchbase
cbbackupmgr config -a /data/backup_migrate -r cluster --disable-data

gsutil -m cp -r gs://cb_backup/cluster/* /data/backup_migrate/cluster/

cbbackupmgr restore -a /data/backup_migrate  -r cluster -c http://127.0.0.1:8091 \
    -u $CB_REST_USERNAME -p $CB_REST_PASSWORD  --auto-create-buckets
