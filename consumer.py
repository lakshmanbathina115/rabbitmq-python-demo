import pika

# Define credentials
credentials = pika.PlainCredentials('guest', 'guest')

# Connect to RabbitMQ server
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='localhost',
        port=5672,
        credentials=credentials
    )
)
channel = connection.channel()

# Declare the same queue to ensure it exists
channel.queue_declare(queue='hello')

# Define the callback to run when a message is received
def callback(ch, method, properties, body):
    print(f" [x] Received {body}")
    # Send ACK back to RabbitMQ
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Subscribe to the queue
channel.basic_consume(
    queue='hello',
    on_message_callback=callback,
    auto_ack=False
)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()