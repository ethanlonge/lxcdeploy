import sys
import pylxd

if (len(sys.argv) > 1):
    lxd = pylxd.Client()
    container = lxd.containers.get(sys.argv[1])
    state = container.state()
    net = state.network.get("eth0")
    print(net["addresses"][1]["address"])