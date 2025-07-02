# RabbitMQ Python Demo — All Exchange Types

This project demonstrates how to publish and consume messages in RabbitMQ using Python, for **all four major exchange types.**

✅ **Exchanges supported:**
- Direct
- Fanout
- Topic
- Headers

Both producer and consumer are implemented in:
- `producer.py`
- `consumer.py`

You can dynamically test routing keys and headers via command-line arguments.

---

## 🔹 1. Direct Exchange

**Use Case:**  
Routes messages to queues with an **exact routing key.**

✅ **Example:**
- Producer sends:
    ```
    routing_key = "info"
    message = "User logged in!"
    ```
- Only consumers bound to `info` receive it.

### Run:

**Consumer:**
```bash
python consumer.py direct info
```

**Producer:**
```bash
python producer.py direct "User logged in!" info
```

---

## 🔹 2. Fanout Exchange

**Use Case:**  
Broadcast messages to **all queues** bound to the exchange.

✅ **Example:**
- Producer sends:
    ```
    message = "System maintenance at midnight"
    ```
- All consumers receive it.

### Run:

**Start multiple consumers:**
```bash
python consumer.py fanout
python consumer.py fanout
python consumer.py fanout
```

**Producer:**
```bash
python producer.py fanout "System maintenance at midnight"
```

---

## 🔹 3. Topic Exchange

**Use Case:**  
Routes messages based on wildcard patterns in routing keys.

✅ **Example:**
- Routing keys:
    - `logs.info`
    - `logs.error`
- Consumer bound to:
    ```
    logs.*
    ```
→ Receives all logs.

### Run:

**Consumer:**
```bash
python consumer.py topic logs.*
```

**Producer:**
```bash
python producer.py topic "An error occurred!" logs.error
```

---

## 🔹 4. Headers Exchange

**Use Case:**  
Routes messages based on **headers** instead of routing keys.

✅ **Example:**
- Producer sends:
    ```
    headers = {"format": "pdf"}
    message = "PDF document uploaded"
    ```
- Only consumers bound to headers matching `format=pdf` will receive it.

### Run:

**Consumer:**
```bash
python consumer.py headers '{"x-match":"all","format":"pdf"}'
```

**Producer:**
```bash
python producer.py headers "PDF document uploaded" '{"format":"pdf"}'
```

---