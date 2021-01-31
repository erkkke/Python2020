import pika
import sys
import pika
from threading import Thread

class Producer(Thread):
    def run(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

        severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
        message = ' '.join(sys.argv[2:]) or 'Hello World!'
        channel.basic_publish(
            exchange='direct_logs', routing_key=severity, body=message)
        print(" [x] Sent %r:%r" % (severity, message))
        connection.close()

class Consumer(Thread):
    def run(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        severities = sys.argv[1:]
        if not severities:
            sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
            sys.exit(1)

        for severity in severities:
            channel.queue_bind(
                exchange='direct_logs', queue=queue_name, routing_key=severity)

        print(' [*] Waiting for logs. To exit press CTRL+C')


        def callback(ch, method, properties, body):
            print(" [x] %r:%r" % (method.routing_key, body))


        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)

        channel.start_consuming()

producer = Producer()
consumer = Consumer()

producer.start()
consumer.start()