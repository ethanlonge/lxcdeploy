#/etc/netplan/10-ens3.yaml

import yaml
import sys
import subprocess
import os

prefix = os.environ["config_networking_ipv6_prefix"]
container_prefix = os.environ["config_networking_ipv6_container_prefix"]

with open("/etc/netplan/10-ens3.yaml") as netplan:
    np = yaml.load(netplan, Loader=yaml.FullLoader)
    ip = ""
    if (len(sys.argv) < 2):
        for i in range(0x1, 0xffff):
            if (prefix + container_prefix + format(i, 'x') + "/64") not in np["network"]["ethernets"]["ens3"]["addresses"]:
                break
        ip = prefix + container_prefix + format(i, 'x')
    else:
        ip = prefix + sys.argv[1]
    np["network"]["ethernets"]["ens3"]["addresses"].append(ip + "/64")

with open("/etc/netplan/10-ens3.yaml", "w") as netplan:
    yaml.dump(np, netplan)

subprocess.call(["sudo", "netplan", "apply"])

print(ip + "/128")
