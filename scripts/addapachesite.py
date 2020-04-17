import sys
import subprocess
import os

ipv6 = sys.argv[1]
name = sys.argv[2]
fqdn = os.environ["config_networking_fqdn"]

config = """
<VirtualHost *:80>
        ServerName {name}.{fqdn}
        ProxyPass / http://{ipv6}/
        ProxyPassReverse / http://{ipv6}/
</VirtualHost>\n
<VirtualHost *:443>
        ServerName {name}.{fqdn}
        ProxyPass / https://{ipv6}/
        ProxyPassReverse / https://{ipv6}/
</VirtualHost>
""".format(ipv6=ipv6, name=name, fqdn=fqdn)

sitefile = open("/etc/apache2/sites-enabled/010-" + name + ".conf", "w")
sitefile.write(config)

subprocess.call(["service", "apache2", "reload"])
