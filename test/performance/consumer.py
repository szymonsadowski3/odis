import pika
import json

from src.amqp.json_to_sql_insert_converter import convert_json_to_sql_insert
from src.rest_api.db.db_configuration import get_connection
import os


def set_up():
    os.environ['IS_TEST'] = 'True'
    print("setting up database stuff...")
    connection = get_connection()
    connection.autocommit = True
    global db_cursor
    db_cursor = connection.cursor()
    cursor = db_cursor
    cursor.execute("CREATE SCHEMA IF NOT EXISTS test")
    cursor.execute("SET search_path TO test")
    cursor.execute("DROP TABLE IF EXISTS ip_traffic;")
    cursor.execute("""
            create table ip_traffic
            (
                event_type varchar(255),
                ip_src varchar(255),
                ip_dst varchar(255),
                port_src varchar(255),
                port_dst varchar(255),
                timestamp_start timestamp,
                timestamp_end timestamp,
                packets integer,
                bytes integer,
                writer_id varchar(255),
                mac_src varchar(255),
                mac_dst varchar(255),
                ip_proto varchar(255),
                src_hostname varchar(255),
                dst_hostname varchar(255),
                incoming_outgoing varchar(255)
            );
    """)
    print("Finished setup!")


def consume_rabbit_data_callback(ch, method, properties, body):
    global db_cursor
    print("received callback {} {} {}", ch, method, properties)
    body_decoded = body.decode("utf-8")
    json_parsed = json.loads(body_decoded)

    insert_query = convert_json_to_sql_insert([json_parsed], 'ip_traffic')
    print('Inserting...')
    db_cursor = connection.cursor()
    db_cursor.execute(insert_query)


def main():
    connection = get_connection()
    connection.autocommit = True

    EXCHANGE_NAME = 'test'

    queue_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = queue_connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name)

    channel.basic_consume(queue=queue_name, on_message_callback=consume_rabbit_data_callback, auto_ack=True)

    channel.start_consuming()


if __name__ == "__main__":
    os.environ['IS_TEST'] = 'True'
    set_up()
    connection = get_connection()
    connection.autocommit = True
    db_cursor = connection.cursor()
    main()
