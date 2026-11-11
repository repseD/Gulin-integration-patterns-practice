import json

from main import QUEUE_ESTIMATES, QUEUE_REQUESTS, connect, declare_all

REQUEST = {
    "request_id": "R-001",
    "well": "Скважина №57",
    "initiator": "Гулин Глеб Владимирович",
    "works": [
        {"type": "drilling", "depth_m": 300},
        {"type": "electrical", "points": 12},
        {"type": "logistics", "distance_km": 650},
    ],
}


def on_estimate(channel, method, properties, body):
    print("[initiator] Получена сводная смета:")
    print(json.dumps(json.loads(body), indent=2, ensure_ascii=False))
    channel.basic_ack(method.delivery_tag)


if __name__ == "__main__":
    channel = connect().channel()
    declare_all(channel)
    channel.basic_consume(QUEUE_ESTIMATES, on_estimate)
    channel.basic_publish("", QUEUE_REQUESTS, json.dumps(REQUEST, ensure_ascii=False).encode())
    print(f"[initiator] Заявка {REQUEST['request_id']} отправлена, жду смету...")
    channel.start_consuming()
