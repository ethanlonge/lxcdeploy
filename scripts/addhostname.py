#thyme.mango.vsys.ml.            300     IN      AAAA  2001:19f0:5801:dd8:1337:420:69:1

import subprocess
import sys
import os

server = os.environ["config_networking_fqdn"]
publicip = os.environ["config_networking_ipv4"]
ttl = os.environ["config_networking_dns_ttl"]
nsdb_location = os.environ["config_networking_dns_zone_db"]

i6prefix = "6."

name = sys.argv[1]
ip = sys.argv[2]

with open(nsdb_location, "a") as nsdb:
    nsdb.write("\n" +
               name + "." + server + ".            " + ttl + "     IN      AAAA  " + ip + "\n" +
               name + "." + server + ".            " + ttl + "     IN      A     " + publicip + "\n" +
               name + "." + i6prefix + server + ".            " + ttl + "     IN      AAAA  " + ip + "\n")

subprocess.call(["sudo", "rndc", "reload", server], stdout=subprocess.PIPE)

print(name + "." + i6prefix + server)
print(name + "." + server)