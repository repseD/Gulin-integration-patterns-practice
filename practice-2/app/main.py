import os

from pika import BlockingConnection, ConnectionParameters

RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")

QUEUE_REQUESTS = "repair.requests"      # инициатор -> оркестратор
QUEUE_REPLIES = "calculations.replies"  # исполнители -> оркестратор
QUEUE_ESTIMATES = "repair.estimates"    # оркестратор -> инициатор

WORKER_QUEUES = {
    "drilling": "drilling.requests",
    "electrical": "electrical.requests",
    "logistics": "logistics.requests",
}

ALL_QUEUES = [QUEUE_REQUESTS, QUEUE_REPLIES, QUEUE_ESTIMATES, *WORKER_QUEUES.values()]


def connect():
    return BlockingConnection(ConnectionParameters(host=RABBIT_HOST))


def declare_all(channel):
    """Объявить все очереди (идемпотентно), чтобы публикатор не потерял сообщения."""
    for queue in ALL_QUEUES:
        channel.queue_declare(queue=queue)
