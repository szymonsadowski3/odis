import pika
import json

from src.amqp.json_to_sql_insert_converter import convert_json_to_sql_insert
from src.rest_api.db.db_configuration import get_connection

# Set postgres connection for autocommit
connection = get_connection()
connection.autocommit = True


EXCHANGE_NAME = 'fanoucik'

queue_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = queue_connection.channel()

channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name)


def callback(ch, method, properties, body):
    body_decoded = body.decode("utf-8")
    json_parsed = json.loads(body_decoded)

    insert_query = convert_json_to_sql_insert([json_parsed], 'ip_traffic')
    print('Inserting...')
    db_cursor = connection.cursor()

    db_cursor.execute(insert_query)


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()

