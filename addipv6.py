#/etc/netplan/10-ens3.yaml

import yaml
import sys
import subprocess

with open("/etc/netplan/10-ens3.yaml") as netplan:
    np = yaml.load(netplan, Loader=yaml.FullLoader)
    ip = ""
    if (len(sys.argv) < 2):
        for i in range(0x1, 0xffff):
            if (prefix + "1337:0420:0069:" + format(i, 'x') + "/64") not in np["network"]["ethernets"]["ens3"]["addresses"]:
                break
        ip = prefix + "1337:0420:0069:" + format(i, 'x')
    else:
        ip = prefix + sys.argv[1]
    np["network"]["ethernets"]["ens3"]["addresses"].append(ip + "/64")

with open("/etc/netplan/10-ens3.yaml", "w") as netplan:
    yaml.dump(np, netplan)

subprocess.call(["sudo", "netplan", "apply"])

print(ip + "/128")
