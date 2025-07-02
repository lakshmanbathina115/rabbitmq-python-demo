import pika
import sys
import json

EXCHANGES = {
    "direct": {
        "type": "direct",
        "exchange": "direct_logs",
    },
    "fanout": {
        "type": "fanout",
        "exchange": "logs_fanout",
    },
    "topic": {
        "type": "topic",
        "exchange": "topic_logs",
    },
    "headers": {
        "type": "headers",
        "exchange": "headers_logs",
    }
}

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print(" python consumer.py <exchange_type> [binding_key or headers_json]")
        sys.exit(1)

    exchange_type = sys.argv[1]
    extra = sys.argv[2] if len(sys.argv) > 2 else None

    if exchange_type not in EXCHANGES:
        print(f"Unknown exchange type: {exchange_type}")
        sys.exit(1)

    config = EXCHANGES[exchange_type]

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            credentials=pika.PlainCredentials('guest', 'guest')
        )
    )
    channel = connection.channel()

    channel.exchange_declare(
        exchange=config["exchange"],
        exchange_type=config["type"]
    )

    # Default queue name
    queue_name = None

    if exchange_type == "fanout":
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=config["exchange"], queue=queue_name)

    elif exchange_type in ["direct", "topic"]:
        binding_key = extra if extra else ""
        queue_name = f"{exchange_type}_queue_{binding_key.replace('.', '_')}"
        channel.queue_declare(queue=queue_name)
        channel.queue_bind(
            exchange=config["exchange"],
            queue=queue_name,
            routing_key=binding_key
        )

    elif exchange_type == "headers":
        if not extra:
            print("Provide headers as JSON string for headers exchange")
            sys.exit(1)
        headers = json.loads(extra)
        queue_name = "headers_queue_" + "_".join(f"{k}-{v}" for k, v in headers.items())
        channel.queue_declare(queue=queue_name)
        channel.queue_bind(
            exchange=config["exchange"],
            queue=queue_name,
            arguments=headers
        )

    def callback(ch, method, properties, body):
        print(f"[x] Received on {exchange_type} exchange: {body.decode()}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)

    print(f"[*] Waiting for messages on {exchange_type} exchange, queue: {queue_name}")
    channel.start_consuming()

if __name__ == "__main__":
    main()
