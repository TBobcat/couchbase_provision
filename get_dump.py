import sys

from couchbase.cluster import Cluster, ClusterOptions
from couchbase_core.cluster import PasswordAuthenticator
from couchbase.management.users import UserManager
from couchbase.management.buckets import BucketManager
from couchbase.management.admin import Admin
from couchbase.management.users import Role, User, UpsertUserOptions
from couchbase.auth import AuthDomain
from couchbase import *
import json
from vars import *



pa = PasswordAuthenticator('Administrator', 'password')
src_cluster = Cluster(my_cb_url, ClusterOptions(pa))


# put this into a function later
# bucket = src_cluster.bucket('beer-sample')

admin = Admin('Administrator', 'password', my_cb_ip)

src_user_mgr = UserManager(admin)
src_users = src_user_mgr.get_all_users()


dest_admin = Admin('Administrator', 'password', dest_ip)
dest_user_mgr = UserManager(dest_admin)


## print to make sure dest manager works 
print(dest_user_mgr.get_all_users()) 

print("users are:\n")
for user_meta in src_users:
  print(user_meta, "\n")
  print(user_meta.user.username)
  
  # print python obj to json
  print(json.dumps(user_meta.raw_data, indent = 4))
  
  for role_origin in user_meta.effective_roles:
    print(role_origin.role.to_server_str())
    print(role_origin.role.name, role_origin.role.bucket, '\n')

    dest_role_list = [ Role(name=role_origin.role.name, bucket=role_origin.role.bucket) ]

    # insert that user in destination cluster
    dest_user_mgr.upsert_user(
                              User(username=user_meta.user.username, roles=dest_role_list, password="password"),
                              UpsertUserOptions(domain_name="local")
    )



