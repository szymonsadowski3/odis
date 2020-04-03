import json

import psycopg2
from psycopg2.extras import RealDictCursor

from src.rest_api.db.config import DEFAULTS
from src.rest_api.db.db_configuration import connection


TABLE_NAME = 'ip_traffic'
TIMESTAMP_COLUMN = 'timestamp_start'


def get_all_data():
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    query = """SELECT * FROM {0};""".format(TABLE_NAME)

    cursor.execute(query)

    return cursor.fetchall()


def get_all_data_paginated(page, limit):
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    query = """SELECT * FROM {0} OFFSET %s LIMIT %s;""".format(TABLE_NAME)

    cursor.execute(query, (page*limit, limit))

    return cursor.fetchall()


def is_array_empty(filter_param):
    return len(filter_param) == 0


def is_parameter_empty(filter_param):
    return not filter_param or is_array_empty(filter_param)


def get_filtered_data(
        # page, limit, ip_src_in, ip_dst_in, packets_between, bytes_between, stamp_between
    kwargs
):
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    conditions = []
    parameters = []

    in_parameters = ['ip_src_in', 'ip_dst_in']

    for in_parameter in in_parameters:
        if not is_parameter_empty(kwargs[in_parameter]):
            conditions.append("({} IN %s)".format(in_parameter.replace("_in", "")))
            parameters.append(tuple(kwargs[in_parameter]))

    between_numeric_parameters = ['packets_between', 'bytes_between']

    for between_numeric_parameter in between_numeric_parameters:
        extracted_parameter = kwargs[between_numeric_parameter]
        if not is_parameter_empty(extracted_parameter):
            is_upper_unbound = extracted_parameter[1] is None
            conditions.append("({0} BETWEEN %s AND %s{1})".format(
                between_numeric_parameter.replace("_between", ""),
                '::FLOAT8' if is_upper_unbound else ''
            ))
            parameters.append(extracted_parameter[0])
            parameters.append("+infinity" if is_upper_unbound else extracted_parameter[1])

    stamp_between = kwargs["stamp_between"]

    if not is_parameter_empty(stamp_between):
        conditions.append("({} BETWEEN %s AND %s)".format(TIMESTAMP_COLUMN))
        parameters.append(stamp_between[0])
        parameters.append(stamp_between[1] if stamp_between[1] is not None else "'9999-03-27 21:48:02.000000'")

    page = kwargs["page"]
    limit = kwargs["limit"]

    parameters.append(page*limit if limit != DEFAULTS["limit"] else 0)
    parameters.append(limit)

    where_condition = "" if is_array_empty(conditions) else " AND ".join(conditions)

    query = """SELECT * FROM {table_name}
    
    {where}

    {where_condition}
        
        ORDER BY {timestamp_column}
        OFFSET %s LIMIT %s;""".format(
        table_name=TABLE_NAME,
        timestamp_column=TIMESTAMP_COLUMN,
        where='WHERE' if not is_array_empty(conditions) else '',
        where_condition=where_condition
    )

    query_parameters = tuple(parameters)
    cursor.execute(query, query_parameters)

    return cursor.fetchall()


if __name__ == '__main__':
    # get_all_data()
    # result = get_all_data_paginated(1, 20)
    result = get_filtered_data(0, 20, ['172.217.16.130'], [0, None], [0, None], ['2020-03-27 21:02:01.000000', '2020-03-27 21:48:02.000000'])
    print(result)
    # print(len(result))
