import pika
from threading import Thread

class Producer(Thread):
    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='logs', exchange_type='fanout')

        while True:
            message = input()
            channel.basic_publish(exchange='logs', routing_key='', body=message)

        connection.close()


class Consumer(Thread):
    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

        channel = connection.channel()

        channel.exchange_declare(exchange='logs', exchange_type='fanout') # fanout - скидывает инфу всем queue

        result = channel.queue_declare(queue='', exclusive=True) # рандомный queue удаляется после удаления consumera
        queue_name = result.method.queue 

        channel.queue_bind(exchange='logs', queue=queue_name)

        def callback(ch, method, properties, body):
            print(" [x] {}".format(body))

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

        channel.start_consuming()

producer = Producer()
consumer = Consumer()

producer.start()
consumer.start()