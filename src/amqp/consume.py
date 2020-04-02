import pika
import json

EXCHANGE_NAME = 'fanoucik'

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    # b'{"event_type": "purge", "ip_src": "10.0.2.15", "port_src": 37760, "timestamp_start": "2020-04-02 22:40:09.734894", "timestamp_end": "1970-01-01 01:00:00.000000", "packets": 1, "bytes": 40, "writer_id": "default_amqp/28525"}'
    body_decoded = body.decode("utf-8")
    json_parsed = json.loads(body_decoded)

    print(" [x] %r" % body)


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()

