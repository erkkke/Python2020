import pika

def callback(ch, method, properties, body):
    print("Received: {}".format(body))


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.queue_declare(queue='qqq')

channel.basic_consume(queue='qqq', auto_ack='True', on_message_callback=callback)

channel.start_consuming()