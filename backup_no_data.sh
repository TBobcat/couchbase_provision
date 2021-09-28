#!/bin/bash

## run script as a sudoer

set -e

export PATH=/opt/couchbase/bin:$PATH

mkdir /data/backup_migrate

# config backup folder
cbbackupmgr config -a /data/backup_migrate -r cluster --disable-data

# backup the cluster
cbbackupmgr backup -c 127.0.0.1 -u $CB_REST_USERNAME -p $CB_REST_PASSWORD -a /data/backup_migrate -r cluster

# upload backup
gsutil -m cp -r /data/backup_migrate/cluster gs://cb_backup