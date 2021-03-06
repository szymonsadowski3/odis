def convert_json_to_sql_insert(json_array, table_name='tabb'):
    sqlstatement = "INSERT INTO " + table_name + " "

    keylist = ""

    for index, json_item in enumerate(json_array):
        is_first_json = index == 0
        if is_first_json:
            keylist = "("
        valuelist = "("
        first_pair = True
        for key, value in json_item.items():
            if not first_pair:
                if is_first_json:
                    keylist += ", "
                valuelist += ", "
            first_pair = False
            if is_first_json:
                keylist += key
            valuelist += "'{}'".format(str(value))

        if is_first_json:
            keylist += ")"
        valuelist += ")"

        if is_first_json:
            sqlstatement += keylist + " VALUES "
        sqlstatement += valuelist + ", "

    return sqlstatement[:-2]


if __name__ == '__main__':
    res = convert_json_to_sql_insert([
        {"event_type": "purge", "mac_src": "52:54:00:12:35:02", "mac_dst": "08:00:27:51:b8:cb", "ip_src": "151.101.193.69", "port_src": 443, "port_dst": 60596, "ip_proto": "tcp", "timestamp_start": "2020-04-02 23:08:51.885620", "timestamp_end": "1970-01-01 01:00:00.000000", "packets": 1, "bytes": 40, "writer_id": "default_amqp/30944"},
        # {"event_type": "purge", "ip_src": "10.0.2.15", "port_src": 42146, "timestamp_start": "2020-04-02 22:42:01.095830", "timestamp_end": "1970-01-01 01:00:00.000000", "packets": 1, "bytes": 40, "writer_id": "default_amqp/28712"},
    ], 'tabb')
    print(res)
