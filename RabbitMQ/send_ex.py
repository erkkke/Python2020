import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.queue_declare(queue='qqq', durable=True) # durable сохраняет данные в диске

message = ' '.join(sys.argv[1:]) or "Hello World"
channel.basic_publish(exchange='', routing_key='qqq', body=message, properties=pika.BasicProperties(delivery_mode=2)) # сохранение в диске

print("Sent 'EXAMPLE'")
channel.close()