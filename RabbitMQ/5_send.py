import pika
import sys
from threading import Thread

class Producer(Thread):
    def run(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

        routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
        message = ' '.join(sys.argv[2:]) or 'Hello World!'
        channel.basic_publish(
            exchange='topic_logs', routing_key=routing_key, body=message)
        print(" [x] Sent %r:%r" % (routing_key, message))
        connection.close()


class Consumer(Thread):
    def run(self):
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

        result = channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue

        binding_keys = sys.argv[1:]
        if not binding_keys:
            sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
            sys.exit(1)

        for binding_key in binding_keys:
            channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=binding_key)

        print(' [*] Waiting for logs. To exit press CTRL+C')


        def callback(ch, method, properties, body):
            print(" [x] %r:%r" % (method.routing_key, body))


        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

        channel.start_consuming()

producer = Producer()
consumer = Consumer()

producer.start()
consumer.start()