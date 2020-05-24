import unittest
import pika
import json
import os

from src.amqp.consume import consume_rabbit_data_callback
from src.amqp.json_to_sql_insert_converter import convert_json_to_sql_insert
from src.rest_api.db.db_configuration import get_connection
from threading import Thread
from time import sleep


def setUp(self):
    os.environ['IS_TEST'] = 'True'
    print("setting up database stuff...")
    self.connection = get_connection()
    self.connection.autocommit = True
    global db_cursor
    db_cursor = self.connection.cursor()
    self.cursor = db_cursor
    self.cursor.execute("CREATE SCHEMA IF NOT EXISTS test")
    self.cursor.execute("SET search_path TO test")
    self.cursor.execute("DROP TABLE IF EXISTS ip_traffic;")
    self.cursor.execute("""
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

    self.EXCHANGE_NAME = 'test'

    # queue_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    queue_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    self.channel = queue_connection.channel()

    self.channel.exchange_declare(exchange=self.EXCHANGE_NAME, exchange_type='fanout')

    result = self.channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    self.channel.queue_bind(exchange=self.EXCHANGE_NAME, queue=queue_name)

    self.channel.basic_consume(queue=queue_name, on_message_callback=consume_rabbit_data_callback, auto_ack=True)

    self.thread = Thread(target = self.channel.start_consuming)
    self.thread.start()

    def tearDown(self):
        self.thread.join()

    def test_consume_rabbit_data_callback(self):
        # self.assertTrue(True)
        self.channel.basic_publish(exchange='test', routing_key='hello', body=b'{"event_type": "purge", "mac_src": "08:00:27:51:b8:cb", "mac_dst": "52:54:00:12:35:02", "ip_src": "10.0.2.15", "ip_dst": "172.217.23.99", "port_src": 37306, "port_dst": 443, "ip_proto": "tcp", "timestamp_start": "2020-05-22 21:00:31.578200", "timestamp_end": "1970-01-01 01:00:00.000000", "packets": 1, "bytes": 123, "writer_id": "default_amqp/24133"}')



def main():
    unittest.main()


if __name__ == "__main__":
    main()