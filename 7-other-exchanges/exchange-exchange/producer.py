import pika

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='firstexchange', exchange_type='direct')

channel.exchange_declare(exchange='secondexchange', exchange_type='fanout')

channel.exchange_bind('secondexchange', 'firstexchange', routing_key='exchange-exchange')

message = "This message has gone through multiple exchanges"

# Sử dụng routing_key = exchange-exchange sẽ gửi tới second_exchange
# Sử dụng routing_key = paymentsonly sẽ gửi tới consumer-nomarly (paymentsconsumer)

# channel.basic_publish(exchange='firstexchange', routing_key='exchange-exchange', body=message) 
channel.basic_publish(exchange='firstexchange', routing_key='paymentsonly', body=message)

print(f"sent message: {message}")

connection.close()