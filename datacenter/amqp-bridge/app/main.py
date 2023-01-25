#!/usr/bin/env python
import pika, json, sys, os

def connect(host, credentials):
    parameters = pika.ConnectionParameters(host = host, credentials = credentials)
    connection = pika.BlockingConnection(parameters)
    return connection, connection.channel()

def callback(ch, method, properties, body):
    content = json.loads(body)

    match content['type']:
        case 'pickup':
            print('pickup: ok')
            print(content)

        case 'gps':
            print(f"gps: {content['coords']}")

        case 'deliver':
            print('deliver: ok')
            print(content)

        case _:
            print(f"Unknown type: {content['type']}")

    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    try:
        AMQP_SERVER = os.environ['AMQP_SERVER']
    except KeyError:
        print('[error]: `AMQP_SERVER` environment variable required')
        sys.exit(1)

    # Define credentials
    credentials = pika.PlainCredentials('ladmin', '1f18b97c3a7d')

    # Open the channel
    connection, channel = connect(AMQP_SERVER, credentials)

    # Declare the queue
    channel.queue_declare(queue='delivery', durable=True, exclusive=False, auto_delete=False)

    channel.basic_consume(queue='delivery', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        connection.close()

if __name__ == '__main__':
    main()
