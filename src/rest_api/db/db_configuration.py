import psycopg2


from src.rest_api.db.secrets import MASTER_PASS


def get_connection():
    # return psycopg2.connect(database="postgres", user="odis", password="odis", host="127.0.0.1", port="5432")
    return psycopg2.connect(database="postgres", user="postgres", password=MASTER_PASS, host="database-2.cvbvtxjktmxu.eu-central-1.rds.amazonaws.com", port="5432")

