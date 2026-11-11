import json
import math
import os

from main import QUEUE_REPLIES, WORKER_QUEUES, connect, declare_all

SERVICE_TYPE = os.getenv("SERVICE_TYPE")


def calculate(part):
    if part["type"] == "drilling":
        return part["depth_m"] * 2500, math.ceil(part["depth_m"] / 150)
    if part["type"] == "electrical":
        return part["points"] * 3500, math.ceil(part["points"] / 6)
    return part["distance_km"] * 200 + 10000, math.ceil(part["distance_km"] / 500)


def on_part(channel, method, properties, body):
    part = json.loads(body)
    cost, days = calculate(part)
    reply = {"request_id": part["request_id"], "type": part["type"], "cost": cost, "duration_days": days}
    channel.basic_publish("", QUEUE_REPLIES, json.dumps(reply, ensure_ascii=False).encode())
    print(f"[{part['type']}] расчёт готов: {reply}")
    channel.basic_ack(method.delivery_tag)


if __name__ == "__main__":
    channel = connect().channel()
    declare_all(channel)
    channel.basic_consume(WORKER_QUEUES[SERVICE_TYPE], on_part)
    print(f"[{SERVICE_TYPE}] исполнитель запущен")
    channel.start_consuming()
