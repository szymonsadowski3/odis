import pika

from test.performance.config import HOW_MANY_RECORDS_FOR_TEST
from test.test_data.rabbit_data import TEST_IP_TRAFFIC_BODY

EXCHANGE_NAME = 'test'

queue_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = queue_connection.channel()

channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name)

for i in range(HOW_MANY_RECORDS_FOR_TEST):
    channel.basic_publish(exchange=EXCHANGE_NAME, routing_key='hello', body=TEST_IP_TRAFFIC_BODY)