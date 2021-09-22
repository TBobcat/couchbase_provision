## using couchbase sdk 3.2

# needed for any cluster connection
from couchbase.cluster import Cluster, ClusterOptions
from couchbase.auth import PasswordAuthenticator

# needed to support SQL++ (N1QL) query
from couchbase.cluster import QueryOptions

# get a reference to our cluster
cluster = Cluster('couchbase://34.93.231.28', ClusterOptions(
  PasswordAuthenticator('Administrator', 'password')))

# get a reference to our bucket
cb = cluster.bucket('beer-sample')

# default collection for couchbase 6.6 that covers whole bucket
cb_coll = cb.default_collection()

# get document function
def get_airline_by_key(key):
  print("\nGet Result: ")
  try:
    result = cb_coll.get(key)
    print(result.content_as[str])
  except Exception as e:
    print(e)

get_airline_by_key("21st_amendment_brewery_cafe")
# result = cb_coll.get("21st_amendment_brewery_cafe")
# print(result.content_as[dict])

