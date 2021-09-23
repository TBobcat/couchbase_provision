#!/bin/bash

## run script as a sudoer

export PATH=/opt/couchbase/bin:$PATH

mkdir /data/backup

# config backup folder
cbbackupmgr config -a /data/backup -r cluster --disable-data

# backup the cluster
cbbackupmgr backup -c 127.0.0.1 -u Administrator -p password -a /data/backup -r cluster

# upload backup
gsutil cp -r /data/backup/cluster gs://cb_backup