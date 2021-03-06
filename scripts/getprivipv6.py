import sys
import pylxd


def getPrivIPv6():
    eth0 = pylxd.Client().containers.get(sys.argv[1]).state().network.get("eth0")
    for address in eth0["addresses"]:
        if address["family"] == "inet6" and address["scope"] == "global":
            return address["address"]
    return ""

if (len(sys.argv) > 1):
    ip = "" 
    while ip == "":
        ip = getPrivIPv6()
    print(ip)
