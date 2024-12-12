import logging
import tornado.ioloop
import tornado.web
import tornado.websocket
import redis.asyncio as aioredis
import json
import asyncio
import webbrowser

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("server_logs.log"),
        logging.StreamHandler()
    ]
)

# Асинхронный Redis клиент
async_redis_client = aioredis.Redis()

# Словарь активных WebSocket подключений
active_connections = {}

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.username = self.get_argument("username", f"User_{len(active_connections) + 1}")
        active_connections[self.username] = self
        self.notify_user_list()
        logging.info(f"{self.username} connected")

        self.write_message(json.dumps({
            "type": "system",
            "message": f"Привет, {self.username}! Добро пожаловать в чат"
        }))

    async def on_message(self, message):
        logging.info(f"Message from {self.username}: {message}")
        await async_redis_client.publish("chat", json.dumps({
            "type": "message",
            "user": self.username,
            "text": message
        }))

    def on_close(self):
        if self.username in active_connections:
            del active_connections[self.username]
        self.notify_user_list()
        logging.info(f"{self.username} disconnected")

    def notify_user_list(self):
        current_users = list(active_connections.keys())
        logging.info(f"Active users: {current_users}")
        message = json.dumps({
            "type": "update_users",
            "users": current_users
        })
        for conn in active_connections.values():
            conn.write_message(message)

    def check_origin(self, origin):
        return True

async def redis_listener():
    pubsub = async_redis_client.pubsub()
    await pubsub.subscribe("chat")
    logging.info("Listening for Redis messages")

    async for msg in pubsub.listen():
        if msg["type"] == "message":
            message = msg["data"].decode("utf-8") if isinstance(msg["data"], bytes) else msg["data"]
            logging.info(f"Redis message: {message}")
            for conn in active_connections.values():
                await conn.write_message(message)

class MainPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/index.html")

def make_app():
    return tornado.web.Application([
        (r"/", MainPageHandler),
        (r"/ws", WebSocketHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "./static"})
    ])

# Запуск сервера
if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    logging.info("Server running at http://localhost:8888")
    webbrowser.open("http://localhost:8888")

    # Запуск Redis слушателя
    loop = asyncio.get_event_loop()
    loop.create_task(redis_listener())

    tornado.ioloop.IOLoop.current().start()