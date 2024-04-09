# 3DiVi тестовое задание
Для запуска создал docker-compose.yaml
## Клиент
Для асинхронного клиента создан DockerfileClient.\
Клиент реализован на основе FastAPI. \
Для запуска запустить контейнер. Переменные окружения не требуются. \
Отправляет задачу в RabbitMQ.

Docker = DockerfileClient
## Сервер
### Асинхронный сервис-приемщик
Реализован на основе FastAPI.\

Имеет один маршрут "setTask" \
Принимает данные о id задачи и времени её задержки \

Docker - DockerfileReceiver
### Сервис-обработчик запросов
Реализован при помощи брокера сообщений RabbitMQ \

Docker - DockerfileHandler
### Сервис записи
Реализован на основе FastAPI.\

Имеет два маршрута \
- "writeTaskFirst" - Записываем данные в формате: | id | receive_time | write_time |
- "writeTaskSecond" - Записываем данные в формате: | id | receive_time |

- Docker - DockerfileWriter