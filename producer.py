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
    if len(sys.argv) < 3:
        print("Usage:")
        print(" python producer.py <exchange_type> <message> [routing_key or headers_json]")
        sys.exit(1)

    exchange_type = sys.argv[1]
    message = sys.argv[2]
    extra = sys.argv[3] if len(sys.argv) > 3 else None

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

    routing_key = ""
    properties = None

    if exchange_type in ["direct", "topic"]:
        routing_key = extra if extra else ""
    elif exchange_type == "headers":
        if not extra:
            print("Provide headers as JSON string for headers exchange")
            sys.exit(1)
        headers = json.loads(extra)
        properties = pika.BasicProperties(headers=headers)

    channel.basic_publish(
        exchange=config["exchange"],
        routing_key=routing_key,
        body=message,
        properties=properties
    )

    print(f"[x] Sent message to {exchange_type} exchange: {message}")
    connection.close()

if __name__ == "__main__":
    main()