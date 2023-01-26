#!/usr/bin/env python
import pika, requests, json, sys, os

def connect(host, credentials):
    parameters = pika.ConnectionParameters(host = host, credentials = credentials)
    connection = pika.BlockingConnection(parameters)
    return connection, connection.channel()

def callback(ch, method, properties, body):
    content = json.loads(body)

    match content['type']:
        case 'pickup':
            payload = {
                'status': 'pick up',
                'deliver_id': content['deliver_id'],
                'timestamp': content['timestamp']
            }
            send(content['package_id'], payload)

        case 'gps':
            for package in content['package_list']:
                payload = {
                    'status': 'in delivery',
                    'coords': content['coords'],
                    'deliver_id': content['deliver_id'],
                    'timestamp': content['timestamp']
                }
                send(package, payload)

        case 'deliver':
            payload = {
                'status': content['status'],
                'deliver_id': content['deliver_id'],
                'timestamp': content['timestamp']
            }
            send(content['package_id'], payload)
            delete(content['package_id'])

        case _:
            print(f"Unknown type: {content['type']}")

    ch.basic_ack(deliver_tag=method.deliver_tag)

def send(package_id, payload):
    try:
        r = requests.put(f"http://octopus:8000/packages/{package_id.lower()}", json=payload)
        r.raise_for_status()
    # except requests.HTTPError as error:
    #     print("The video library already exists.") if r.status_code == 409 else print(error)
    except requests.RequestException as error:
        print(error)

def delete(package_id):
    try:
        r = requests.delete(f"http://octopus:8000/packages/{package_id.lower()}")
        r.raise_for_status()
    # except requests.HTTPError as error:
    #     print("The video library does not exist.") if r.status_code == 404 else print(error)
    except requests.RequestException as e:
        print(error)

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
