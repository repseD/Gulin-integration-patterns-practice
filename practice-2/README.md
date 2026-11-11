Гулин Глеб Владимирович
Практика 2

Паттерны:
Composed Message Processor (основной) - orchestrator
Splitter - заявка
Message Router - подзаявка
Aggregator - расчёты

Запуск:
docker compose up --build

Логи:
docker compose logs -f initiator

UI RabbitMQ: http://localhost:15672 (guest/guest)
