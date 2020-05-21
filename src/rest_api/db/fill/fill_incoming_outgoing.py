from src.rest_api.db.db_configuration import get_connection
import re

import sh

connection = get_connection()


def get_local_network_ip_addresses():
    ifconfig_result = sh.ifconfig()
    ifconfig_result_str = ifconfig_result.stdout.decode("utf-8")
    ips = re.findall(r'[0-9]+(?:\.[0-9]+){3}', ifconfig_result_str)
    return ips


connection.autocommit = True


def fill_incoming_outgoing():
    cursor = connection.cursor()
    local_network_ip_addresses = get_local_network_ip_addresses()

    query = """UPDATE ip_traffic
    SET
    incoming_outgoing = 'outgoing'
    WHERE
    ip_src IN %s """

    cursor.execute(query, (tuple(local_network_ip_addresses),))

    # OUTGOING ---

    query = """UPDATE ip_traffic
    SET
    incoming_outgoing = 'incoming'
    WHERE
    ip_dst IN %s """

    cursor.execute(query, (tuple(local_network_ip_addresses),))


fill_incoming_outgoing()
