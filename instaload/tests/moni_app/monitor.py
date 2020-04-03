#!/usr/bin/env python
import json
import pika
import bernhard
import snappy

def receiving():
    """establish connections to receive messages from server"""

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='logs', queue=queue_name)

    print(' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        """callback when a message/body is received"""

        print(" [x] received %r" % body)
        # send requests to riemann
        c = bernhard.Client(host='localhost', port=5555)
        # convert back to dict before send through
        message = snappy.uncompress(body)
        c.send(json.loads(message))

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

if __name__ == '__main__':
    receiving()