#!/usr/bin/env python
import pika, json, sys, os

def create_channel(server):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=server))
        return connection, connection.channel()
    except:
        sys.exit(1)

def callback(ch, method, properties, body):
    content = json.loads(body.decode())
    match content['type']:
        case 'pickup':
            print('ok: pickup')

        case 'gps':
            print('ok: gps')

        case 'deliver':
            print('ok: deliver')

        case _:
            print(f"Unknown type : {content.type}")

def main():
    try:
        AMQP_SERVER = os.environ['AMQP_SERVER']
    except KeyError:
        print('[error]: `AMQP_SERVER` environment variable required')
        sys.exit(1)

    connection, channel = create_channel(AMQP_SERVER)

    channel.queue_declare(queue='delivery')
    channel.basic_consume(queue='delivery', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()
