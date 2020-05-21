import os

import psycopg2


from src.rest_api.db.secrets import MASTER_PASS

env = "local"


def get_connection():
    if os.environ.get('IS_TEST', 'False') == 'True':
        return psycopg2.connect(database="postgres", user="odis", password="odis", host="127.0.0.1", port="5432", options=f'-c search_path=test')

    if env == "local":
        return psycopg2.connect(database="postgres", user="odis", password="odis", host="127.0.0.1", port="5432")
    return psycopg2.connect(database="postgres", user="postgres", password=MASTER_PASS, host="database-2.cvbvtxjktmxu.eu-central-1.rds.amazonaws.com", port="5432")
