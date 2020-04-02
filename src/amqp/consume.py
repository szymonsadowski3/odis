import pika
import json

from src.amqp.json_to_sql_insert_converter import convert_json_to_sql_insert

EXCHANGE_NAME = 'fanoucik'

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    body_decoded = body.decode("utf-8")
    json_parsed = json.loads(body_decoded)

    print(" [x] %r" % json_parsed)
    print(convert_json_to_sql_insert([json_parsed]))


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()

