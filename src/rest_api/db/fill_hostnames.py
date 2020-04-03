from src.rest_api.db.db_configuration import connection

from dns import resolver
from dns import reversename


def reverse_dns_lookup(ip):
    try:
        addr = reversename.from_address(ip)
        return resolver.query(addr, "PTR")[0]
    except Exception as e:
        print(e)
        return None


connection.autocommit = True


def fill_hostname(src_or_dst):
    cursor = connection.cursor()
    query = """SELECT DISTINCT ip_{} FROM ip_traffic;""".format(src_or_dst)
    cursor.execute(query)
    results = cursor.fetchall()
    for distinct_ip in results:
        ip_src = distinct_ip[0]
        reverse_lookup_result = reverse_dns_lookup(ip_src)
        if reverse_lookup_result:
            query = """UPDATE ip_traffic
        SET
        {2}_hostname = '{0}'
        WHERE
        ip_{2} = '{1}';""".format(reverse_lookup_result, ip_src, src_or_dst)

            cursor.execute(query)


fill_hostname('src')
# fill_hostname('dst')
