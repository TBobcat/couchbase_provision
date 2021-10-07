# couchbase_setup_scripts

## Prerequisites:
A GCP bucket that stores a GCP no data backup, and a Service account for staging cluster vm to access that bucket
Shell scripts need to be run on staging cluster and new cluster respectively, before running the user migration python scripts  
Couchbase user credential that has Data backup and Restore role for commands in shell script, DBA.’s user credentials likely will have this.
Terraform should be run through GCP cloudbuild pipeline to spin up VMs.
DBA laptop should have python3 installed.
DBA laptop should be able to hit both staging, and production cluster ips.

## How to Install python3:  
install python3.9 and couchbase module on windows, for python3.9
            Refer to https://www.python.org/downloads/windows/  
Verify in powershell.     
python -V.  
python -m pip install couchbase         

## VM requirements:
Linux sudoer to run shell script

## Provisioning Steps:
   — Devops:	
- Run terraform code to spin up cluster  

— DBA:					  
- Go in couchbase cluster, click rebalance
- Pull the repo to the laptop
			    
- Fill in couchbase admin user credentials in cred.sh                             
- Run backup couchbase shell script on a server on the new cluster   
  . cred.sh.  
  bash ./restore_no_data.sh
- Run restore couchbase shell script on a server on the new cluster   
  . cred.sh.  
  bash ./restore_no_data.sh
- Fill in vars.py
- Run python3 get_users.py 

The script will output each local Couchbase user and their roles, wait for it to finish.
Note: All destination users will have the default couchbase password.
