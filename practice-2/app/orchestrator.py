import json

from main import QUEUE_ESTIMATES, QUEUE_REPLIES, QUEUE_REQUESTS, WORKER_QUEUES, connect, declare_all

pending = {}


def on_request(channel, method, properties, body):
    request = json.loads(body)
    rid = request["request_id"]
    pending[rid] = {
        "well": request["well"],
        "initiator": request["initiator"],
        "expected": len(request["works"]),
        "items": [],
    }
    print(f"[splitter] Заявка {rid}: {[w['type'] for w in request['works']]}")
    for work in request["works"]:
        queue = WORKER_QUEUES[work["type"]]
        part = {"request_id": rid, **work}
        channel.basic_publish("", queue, json.dumps(part, ensure_ascii=False).encode())
        print(f"[router] {work['type']} -> {queue}")
    channel.basic_ack(method.delivery_tag)


def on_reply(channel, method, properties, body):
    reply = json.loads(body)
    p = pending[reply["request_id"]]
    p["items"].append(reply)
    print(f"[aggregator] Получен расчёт: {reply['type']}")
    if len(p["items"]) == p["expected"]:
        items = p["items"]
        estimate = {
            "request_id": reply["request_id"],
            "well": p["well"],
            "initiator": p["initiator"],
            "items": items,
            "total_cost": sum(i["cost"] for i in items),
            "total_days": sum(i["duration_days"] for i in items),
        }
        channel.basic_publish("", QUEUE_ESTIMATES, json.dumps(estimate, ensure_ascii=False).encode())
        print(f"[aggregator] Смета {reply['request_id']} отправлена инициатору")
    channel.basic_ack(method.delivery_tag)


if __name__ == "__main__":
    channel = connect().channel()
    declare_all(channel)
    channel.basic_consume(QUEUE_REQUESTS, on_request)
    channel.basic_consume(QUEUE_REPLIES, on_reply)
    print("[orchestrator] Запущен, жду заявки...")
    channel.start_consuming()
