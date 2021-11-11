# couchbase_setup_scripts
This repository holds scripts to migrate buckets, views, indexes, and users without migrating actual data from a staging couchbase cluster to a production cluster. 

User migration script uses python3, and hits api end points of both clusters.
Buckets, views, indexes migration is done through shell scripts that essentially runs couchbase-cli commands. Scripts uploads these into a cloud storage bucket and the new prod. cluster can download and restore from it.

## Prerequisites:

### Connections:
* DBA laptop should be able to hit both staging, and production cluster ips. In addition, for the user migration script to work, all ports need to be opened [here.](https://docs.couchbase.com/server/current/install/install-ports.html) A firewall rule is specified in terraform, and can be modified to limite the source ip range that hits these ports.

```
resource "google_compute_firewall" "couchbase_fw" {
  name    = "couchbase-private"
  network = google_compute_network.dev_vpc.name

  // If neither targetServiceAccounts nor targetTags are specified, the 
  //firewall rule applies to all instances on the specified network.

  // only open to private ips
  // source_ranges = ["10.0.0.0/8", "192.168.0.0/16", "172.16.0.0/12"]

  allow {
    protocol = "tcp"
    ports = [
      // couchbase ui and cluster management ports
      "21100", "21150", "21200",

      // node to node
      "4369",
      "8092-8094", "9100-9105",
      "9110-9118",
      "9120-9122",
      "9130",
      "9999", "11209-11210",
      "11206", "11207", "19102", "19130",

      // client to node
      "8092-8096", "9140", "11210", "11211",
      "11207", "18091-18096",

      // node-local
      "9119", "9998", "11213", "21200", "21300",
      "21250", "21350"
    ]
  }
}
```
* Couchbase requires to set alternate address name for external ip api connection. More can be found [here.](https://docs.couchbase.com/php-sdk/current/howtos/managing-connections.html#alternate-addresses-and-custom-ports)

### Other Prerequisits
A GCP bucket to store the no data backup, and service accounts for both the staging cluster and new prod. cluster that have access to the bucket is required.

Shell scripts need to be run on staging cluster and new cluster respectively, before running the user migration python scripts. This makes sure the buckets will be in place in the prod. cluster so that any user that has roles to those buckets will not get errors while running the user migration scripts.

Couchbase user credential used by the shell scripts will need Data backup and Restore role, DBA.’s user credentials likely will have this.

Terraform should be run through GCP cloudbuild pipeline to spin up VMs.

DBA laptop should have python3, and packages in requirements.txt installed.




## How to Install python3:  
install python3.9 and couchbase module on windows, for python3.9
            Refer to https://www.python.org/downloads/windows/  
Verify in powershell.     
python3 -V.  
python3 -m pip install couchbase         
python3 install -r requirements.txt

## VM requirements:
Linux sudoer to run shell script

## Provisioning Steps:
   — DevOps:	
- Run terraform code to spin up cluster  

— DBA:					  
- Go in couchbase cluster, click rebalance
- Pull this repo to the laptop
			    
- Fill in couchbase admin user credentials in `backup_no_data.sh` and `restore_no_data.sh`.

- Run backup couchbase shell script on a server on the staging cluster as a sudoer  
  bash ./backup_no_data.sh
- Run restore couchbase shell script on a server on the new cluster as a sudoer
  bash ./restore_no_data.sh
- Fill in vars.py
- Run python3 get_users.py 

The script will output each local Couchbase user and their roles, wait for it to finish.

Note: All destination users will have the default couchbase password, as credentials migration is not supported by couchbase at the moment
