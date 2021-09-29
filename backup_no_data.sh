#!/bin/bash

## run script as a sudoer

set -e

export PATH=/opt/couchbase/bin:$PATH

rm -rf /tmp/backup_migrate
mkdir /tmp/backup_migrate

# config backup folder
cbbackupmgr config -a /tmp/backup_migrate -r cluster --disable-data

# backup the cluster
cbbackupmgr backup -c 127.0.0.1 -u $CB_REST_USERNAME -p $CB_REST_PASSWORD -a /tmp/backup_migrate -r cluster

# remove older backup, and upload the new one
# put a text file in first run so rm command won't error out
gsutil rm gs://cb_backup/**
gsutil -m cp -r /tmp/backup_migrate/cluster gs://cb_backup