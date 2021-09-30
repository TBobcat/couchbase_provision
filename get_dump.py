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
import traceback
import pprint



pa = PasswordAuthenticator(admin, pwd)
src_cluster = Cluster(source_url, ClusterOptions(pa))

admin = Admin(admin, pwd, source_ip)

src_user_mgr = UserManager(admin)
src_users = src_user_mgr.get_all_users()

## create a user manager for destination cluster
dest_admin = Admin('Administrator', 'password', dest_ip)
dest_user_mgr = UserManager(dest_admin)

# def get_src_users():
#   return

# def get_src_groups():
#   return usr_grps


# def upsert_groups(user_groups):
#   return

for user_meta in src_users:

  # print python obj to json
  print("source users are:\n\n", json.dumps(user_meta.raw_data, indent = 4))
  dest_role_set =set()

  if user_meta.domain.Local == 0:
    for role_origin in user_meta.effective_roles:

      dest_role = role_origin.role
      print("DEST ROLE: \n\n", dest_role.as_dict())
      dest_role_set.add(dest_role)
      
      try:
      # insert that user in destination cluster
        dest_user_mgr.upsert_user(
                                  # there's no way to migrate over user passwords, so this sets it to a temporary one
                                  User(username=user_meta.user.username, roles=dest_role_set, password="password"),
                                  domain_name="local"
        )
      except Exception as e:
        print( "EXCEPTION TRACE  PRINT:\n{}".format( "".join(traceback.format_exception(type(e), e, e.__traceback__))))

  else:
    continue




  



