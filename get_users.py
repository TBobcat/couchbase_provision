import sys

from couchbase.cluster import Cluster, ClusterOptions
from couchbase_core.cluster import PasswordAuthenticator
from couchbase.management.users import UserManager
from couchbase.management.admin import Admin
from couchbase.management.users import User
from couchbase import *
import json
from vars import *
import traceback



pa = PasswordAuthenticator(admin, pwd)
src_cluster = Cluster(source_url, ClusterOptions(pa))

admin = Admin(admin, pwd, source_ip)

src_user_mgr = UserManager(admin)


## create a user manager for destination cluster
dest_admin = Admin('Administrator', 'password', dest_ip)
dest_user_mgr = UserManager(dest_admin)

def get_src_users():
  """
  Function to get all users from the source couchbase cluster
  """
  return src_user_mgr.get_all_users()


def migrate_users(source_users):
  """
  Function to upsert all local couchbase users to the destination couchbase cluster
  passwords of the users are set as default password here
  """

  for user_meta in source_users:
  
    # print python obj to json
    # print("source users are:\n\n", json.dumps(user_meta.raw_data, indent = 4))
    dest_role_set =set()
  
    if user_meta.domain.Local == 0:
      for role_origin in user_meta.effective_roles:
  
        dest_role = role_origin.role
        print("DEST. USER:\n\t", user_meta.user.username + ":\n\t", dest_role.as_dict(), "\n")
        dest_role_set.add(dest_role)
        
        # there's no way to migrate over user passwords, so this sets it to a temporary one
        dest_user = User(username=user_meta.user.username, 
                         display_name=user_meta.user.username,
                         roles=dest_role_set, 
                         password="password")
  
        try:
        # insert that user in destination cluster
          dest_user_mgr.upsert_user(dest_user, domain_name="local")
  
        except Exception as e:
          print( "EXCEPTION TRACE  PRINT:\n{}".format( "".join(traceback.format_exception(type(e), e, e.__traceback__))))
  
    else:
      continue


if __name__ == '__main__':
    src_users = get_src_users()
    migrate_users(src_users)




  



