# RabbitMQ admin panel url

http://localhost:15672

# To run pmacct with RabbitMQ plugin

`sudo pmacctd -P amqp -f rabbit_pmacct_config.cfg`

# Aggregate keys configuration

https://github.com/pmacct/pmacct/blob/master/CONFIG-KEYS

# Start server

export PYTHONPATH=.

forever -c python3 src/rest_api/api.py