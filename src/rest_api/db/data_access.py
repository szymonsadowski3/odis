import json

import psycopg2
from psycopg2.extras import RealDictCursor

connection = psycopg2.connect(database="pmacct", user="odis", password="odis", host="127.0.0.1", port="5432")


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


if __name__ == '__main__':
    # get_all_data()
    result = get_all_data_paginated(1, 10)
    print(result)
