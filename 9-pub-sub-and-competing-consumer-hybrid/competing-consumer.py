import pika
import time
import random

def on_message_received(ch, method, properties, body):
    processing_time = random.randint(1, 6)
    print(f'received: "{body}", will take {processing_time} to process')
    time.sleep(processing_time)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f'finished processing and acknowledged message')

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='pubsub-competing', exchange_type='fanout')

queue = channel.queue_declare(queue='')

channel.basic_qos(prefetch_count=1)

channel.queue_bind(exchange='pubsub-competing', queue=queue.method.queue)

channel.basic_consume(queue=queue.method.queue,
    on_message_callback=on_message_received)

print("Starting Competing Consuming")

channel.start_consuming()