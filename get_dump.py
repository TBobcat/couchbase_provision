import sys

from couchbase.cluster import Cluster, ClusterOptions
from couchbase_core.cluster import PasswordAuthenticator
from couchbase.management.users import UserManager
from couchbase.management.buckets import BucketManager
from couchbase.management.admin import Admin
from couchbase.management.users import Role, User, UpsertUserOptions
from couchbase.auth import AuthDomain
import json


cluster_flm_url = "couchbase://10.119.16.48"
cluster_flm_ip = '10.119.16.48'
my_cb_url = 'couchbase://34.93.38.177'
my_cb_ip = '34.93.38.177'


dest_ip = '34.93.247.43'
pa = PasswordAuthenticator('Administrator', 'password')
cluster = Cluster(my_cb_url, ClusterOptions(pa))


# put this into a function later
bucket = cluster.bucket('beer-sample')
collection = bucket.default_collection()

admin = Admin('Administrator', 'password', my_cb_ip)
bucket_mgr = BucketManager(admin)
buckets = bucket_mgr.get_all_buckets()

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



