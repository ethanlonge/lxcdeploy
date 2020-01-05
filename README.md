# LXCDeploy
This is a simple script that allows the easy creation of LXC/LXD containers for immediate use. This includes:
- Assignment of public IPv6
- Assignment of Hostnames:
    - Hybrid Hostname (IPv4 of host, IPv6 of container) for Apache2 ProxyPass (DIY)
    - IPv6 Only Hostname
- Assignment of random root password
- Enabling of SSH for remote access

## Install
### Requirements
```bash
sudo apt install python3-pip iptables-persistent
sudo pip3 install setuptools wheel
sudo pip3 install -U pyyaml pylxd
```
### BIND Config
If you do not have an existing BIND config, it is recommend you do the following:
Replace server-name, public-ipv4 and public-ipv6 with the correlating information

Bash:
```bash
    apt install bind9
    mkdir /etc/bind/zones
    cp /etc/bind/db.local /etc/bind/zones/db.server-name
```
Edit /etc/bind/named.conf.options:
```
    listen-on-v6 { public-ipv6; };
    listen-on { public-ipv4; }; 
    allow-transfer { none; };
    forwarders { 8.8.8.8; 8.8.4.4 };
```

Edit /etc/bind/named.conf.local:
```
    zone "server-name" {
        type master;
        file "/etc/bind/zones/db.server-name";
    };
```

Edit /etc/bind/zones/db.server-name:
```DNS Zone
    ;
    ; BIND data file for server-name
    ;
    $TTL    604800
    @       IN      SOA     ns1.server-name. admin.server-name. (
                                  3         ; Serial
                             604800         ; Refresh
                              86400         ; Retry
                            2419200         ; Expire
                             604800 )       ; Negative Cache TTL
    ;
                              IN      NS      ns1.server-name.
    ns1.server-name.                      IN      A       public-ipv4
    ns1.server-name.                      IN      AAAA    public-ipv6
    server-name.                          IN      A       public-ipv4
    server-name.                          IN      AAAA    public-ipv6
    txtrec.server-name.      300     IN      TXT   TestConf ; Test Configuration
```

Bash:
```bash
    systemctl restart bind9
    dig txtrec.server-name @public-ipv4 txt +short ; Should output "TestConf" if BIND is working
```

Your DNS Provider:
```
    A ns1.server-name public-ipv4
    NS server-name ns1.server-name
```

Bash:
```bash
    dig txtrec.server-name txt +short ; Should output "TestConf" if your configuration is working
```

### Configuration
To configure the script, rename `sampleconfig.yaml` to `config.yaml` and replace the values.

networking.fqdn: Your fully qualified domain name (for DNS records)
networking.ipv4: Your public IPv4 address of your server
networking.ipv6: Your public IPv6 address of your server
networking.ipv6_prefix: Your IPv6 /64 prefix with trailing colon (eg. "2001:0DB8:DEAD:BEEF:")
networking.ipv6_container_prefix: A prefix for between your public prefix and container number (eg. "1337:0420:0069:")

networking.dns.ttl: The TTL for your DNS records (default is 3600)
networking.dns.zone_db: The location of your BIND zone (eg. "/etc/bind/zones/db.server-name")

container_defaults.image: The default image for the creation of LXD/LXC containers (default is "ubuntu:18.04")