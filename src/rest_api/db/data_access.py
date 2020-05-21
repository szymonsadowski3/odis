from psycopg2.extras import RealDictCursor

from src.rest_api.db.config import DEFAULTS
from src.rest_api.db.db_configuration import get_connection

TABLE_NAME = 'ip_traffic'
TIMESTAMP_COLUMN = 'timestamp_start'


def get_all_data():
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    query = """SELECT * FROM {0};""".format(TABLE_NAME)

    cursor.execute(query)

    return cursor.fetchall()


def get_all_data_paginated(page, limit):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    query = """SELECT * FROM {0} OFFSET %s LIMIT %s;""".format(TABLE_NAME)

    cursor.execute(query, (page*limit, limit))

    return cursor.fetchall()


def is_array_empty(filter_param):
    return len(filter_param) == 0


def is_parameter_empty(filter_param):
    return not filter_param or is_array_empty(filter_param)


def get_filtered_data(
    kwargs
):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    conditions = []
    parameters = []

    in_parameters = ['port_src_in', 'port_dst_in', 'ip_proto_in', 'incoming_outgoing_in']
    contain_parameters = ['ip_src_in', 'ip_dst_in']

    for contain_parameter in contain_parameters:
        if not is_parameter_empty(kwargs[contain_parameter]):
            conditions.append("({} SIMILAR TO %s)".format(contain_parameter.replace("_in", "")))

            parameter = '%({})%'.format('|'.join(kwargs[contain_parameter]))
            '%(foo|bar|baz)%'

            parameters.append(parameter)

    for in_parameter in in_parameters:
        print(in_parameter)
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


def surround_with_quotes(x, quote="'"):
    return "{}{}{}".format(quote, x, quote)


def list_to_pgarray(alist):
    list_formatted = [surround_with_quotes(x, '"') for x in alist]
    return '{{' + ','.join(list_formatted) + '}}'


def insert_class_of_ips(name, ips):
    connection = get_connection()
    connection.autocommit = True
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    query = 'insert into class_of_ips(name, ips) values ({name}, {ips})'.format(
        name=surround_with_quotes(name),
        ips=surround_with_quotes(list_to_pgarray(ips))
    )
    print(query)
    cursor.execute(query)


def delete_class_of_ips(name):
    connection = get_connection()
    connection.autocommit = True
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    query = 'delete from class_of_ips where name = {name}'.format(
        name=surround_with_quotes(name),
    )
    print(query)
    cursor.execute(query)


def edit_class_of_ips(name, ips):
    connection = get_connection()
    connection.autocommit = True
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    query = 'update class_of_ips set ips = {ips} where name = {name}'.format(
        name=surround_with_quotes(name),
        ips=surround_with_quotes(list_to_pgarray(ips))
    )
    print(query)
    cursor.execute(query)


def get_class_of_ips(name):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    query = 'select * from class_of_ips where name = {name}'.format(
        name=surround_with_quotes(name),
    )
    cursor.execute(query)
    return cursor.fetchall()


def get_all_classes_of_ips():
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    query = 'select * from class_of_ips'
    cursor.execute(query)
    return cursor.fetchall()


def get_aggregation(aggregated_column, aggregate_func, aggregate_part, stamp_between):
    where_condition = ""
    query_parameters = []

    if not is_parameter_empty(stamp_between):
        where_condition = "WHERE ({} BETWEEN %s AND %s)".format(TIMESTAMP_COLUMN)
        query_parameters.append(stamp_between[0])
        query_parameters.append(stamp_between[1] if stamp_between[1] is not None else "'9999-03-27 21:48:02.000000'")


    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    query = """SELECT 
        date_trunc('{aggregate_part}', timestamp_start) AS {aggregate_part}, 
        {aggregate_func}({aggregated_column}) AS {aggregated_column}_{aggregate_func}
        FROM ip_traffic 
        {where_condition}
        GROUP BY {aggregate_part};""".format(
        aggregated_column=aggregated_column,
        aggregate_func=aggregate_func,
        aggregate_part=aggregate_part,
        where_condition=where_condition
    )
    cursor.execute(query, tuple(query_parameters))
    return cursor.fetchall()


if __name__ == '__main__':
    # get_all_data()
    # result = get_all_data_paginated(1, 20)
    # result = get_filtered_data(0, 20, ['172.217.16.130'], [0, None], [0, None], ['2020-03-27 21:02:01.000000', '2020-03-27 21:48:02.000000'])
    # print(result)

    # insert_class_of_ips('test', ['111.111.111.111', '222.222.222.222'])
    # edit_class_of_ips('test', ['311.111.111.111', '442.222.222.222'])
    # res = get_class_of_ips('test')
    res = get_all_classes_of_ips()
    # res = find_continuous_streams(['TEST'])
    print(res)
    # print(len(result))
