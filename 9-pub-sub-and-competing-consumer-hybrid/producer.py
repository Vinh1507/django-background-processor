import pika
from pika.exchange_type import ExchangeType
import random
import time

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='pubsub-competing', exchange_type=ExchangeType.fanout)

messageId = 1

while(True):
    message = f"Sending Hybrid Message Id: {messageId}"

    channel.basic_publish(exchange='pubsub-competing', routing_key='', body=message)

    print(f"sent message: {message}")
    
    time.sleep(random.randint(1, 4))

    messageId+=1