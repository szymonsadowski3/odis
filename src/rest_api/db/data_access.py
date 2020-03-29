import json

import psycopg2
from psycopg2.extras import RealDictCursor

from src.rest_api.db.config import DEFAULTS
from src.rest_api.db.db_configuration import connection


def get_all_data():
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    query = """SELECT * FROM acct;"""

    cursor.execute(query)

    return cursor.fetchall()


def get_all_data_paginated(page, limit):
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    query = """SELECT * FROM acct OFFSET %s LIMIT %s;"""

    cursor.execute(query, (page*limit, limit))

    return cursor.fetchall()


def is_array_empty(filter_param):
    return len(filter_param) == 0


def is_parameter_empty(filter_param):
    return not filter_param or is_array_empty(filter_param)


def get_filtered_data(page, limit, ip_src_in, packets_between, bytes_between, stamp_between):
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    conditions = []
    parameters = []

    if not is_parameter_empty(ip_src_in):
        conditions.append("(ip_src IN %s)")
        parameters.append(tuple(ip_src_in))

    if not is_parameter_empty(packets_between):
        is_upper_unbound = packets_between[1] is None
        conditions.append("(packets BETWEEN %s AND %s{0})".format('::FLOAT8' if is_upper_unbound else ''))
        parameters.append(packets_between[0])
        parameters.append("+infinity" if is_upper_unbound else packets_between[1])

    if not is_parameter_empty(bytes_between):
        is_upper_unbound = bytes_between[1] is None
        conditions.append("(bytes BETWEEN %s AND %s{0})".format('::FLOAT8' if is_upper_unbound else ''))
        parameters.append(bytes_between[0])
        parameters.append("+infinity" if is_upper_unbound else bytes_between[1])

    if not is_parameter_empty(stamp_between):
        conditions.append("(stamp_inserted BETWEEN %s AND %s)")
        parameters.append(stamp_between[0])
        parameters.append(stamp_between[1] if stamp_between[1] is not None else "'9999-03-27 21:48:02.000000'")

    parameters.append(page*limit if limit != DEFAULTS["limit"] else 0)
    parameters.append(limit)

    where_condition = "" if is_array_empty(conditions) else " AND ".join(conditions)

    query = """SELECT * FROM acct
    
    {where}

    {where_condition}
        
        ORDER BY stamp_inserted
        OFFSET %s LIMIT %s;""".format(where='WHERE' if not is_array_empty(conditions) else '', where_condition=where_condition)

    query_parameters = tuple(parameters)
    cursor.execute(query, query_parameters)

    return cursor.fetchall()


if __name__ == '__main__':
    # get_all_data()
    # result = get_all_data_paginated(1, 20)
    result = get_filtered_data(0, 20, ['172.217.16.130'], [0, None], [0, None], ['2020-03-27 21:02:01.000000', '2020-03-27 21:48:02.000000'])
    print(result)
    # print(len(result))
