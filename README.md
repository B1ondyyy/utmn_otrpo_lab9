# WEB Chat from Redis

Этот проект представляет собой чат в стиле с использованием WebSocket и Redis для обмена сообщениями в реальном времени.

[![image.png](https://i.postimg.cc/1tqhGFQz/image.png)](https://postimg.cc/ftDrZJk4)

## Описание

Приложение использует:
- **Tornado** для обработки HTTP-запросов и WebSocket-соединений.
- **Redis** для публикации и подписки на сообщения, что позволяет передавать их между различными пользователями в реальном времени.
- **CSS и HTML** для создания интерфейса.

## Логирование

Все события на сервере логируются в файл server.log, где можно отслеживать информацию о подключениях и отправленных сообщениях.

## Установка

Для того чтобы запустить проект локально, выполните следующие шаги:

### 1. Установите зависимости

Убедитесь, что у вас установлены все необходимые библиотеки. Используйте команду:

```bash
pip install -r requirements.txt
```
### 2. Установите и запустите Redis

Проверьте что сервер запущен с помощью команды:

```bash
redis-cli ping
```
В ответ консоль вам должна выдать: PONG

### 3. Запустите сервер

Запустите приложение с помощью команды:

```bash
python main.py
```
## Сервер запустится локально по адресу http://localhost:9999
