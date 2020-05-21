import re

import sh


def get_local_network_ip_addresses():
    ifconfig_result = sh.ifconfig()
    ifconfig_result_str = ifconfig_result.stdout.decode("utf-8")
    ips = re.findall(r'[0-9]+(?:\.[0-9]+){3}', ifconfig_result_str)
    return ips


print(get_local_network_ip_addresses())
