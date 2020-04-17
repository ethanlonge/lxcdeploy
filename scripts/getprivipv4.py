import sys
import pylxd


def getPrivIPv4():
    eth0 = pylxd.Client().containers.get(sys.argv[1]).state().network.get("eth0")
    for address in eth0["addresses"]:
        if address["family"] == "inet" and address["scope"] == "global":
            return address["address"]
    return ""

if (len(sys.argv) > 1):
    ip = ""
    while ip == "":
        ip = getPrivIPv4()
    print(ip)
