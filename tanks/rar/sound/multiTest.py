import pygame
from enum import Enum
import sys
# pylint: disable=no-member
import math
import pika
import uuid
import json
from threading import Thread

IP = '34.254.177.17'
PORT = 5672
VIRTUAL_HOST = 'dar-tanks'
USERNAME = 'dar-tanks'
PASSWORD = '5orPLExUYnyVYZg48caMpX'

pygame.init()
screen = pygame.display.set_mode((1000, 800))


class TankRpcClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=IP,  # СОЗДАЛИ ESTABLISHED CONNECTION
                port=PORT,
                virtual_host=VIRTUAL_HOST,
                credentials=pika.PlainCredentials(
                    username=USERNAME,
                    password=PASSWORD
                )
            )
        )
        self.channel = self.connection.channel()  # CREATING CHANNEL
        queue = self.channel.queue_declare(queue='', exclusive=True, auto_delete=True)  # СОЗДАЕМ АНОНИМНУЮ ОЧЕРЕДЬ
        self.callback_queue = queue.method.queue  # ОЧЕРЕДЬ КУДА ПРИХОДИТ ОТВЕТ
        self.channel.queue_bind(exchange='X:routing.topic',
                                queue=self.callback_queue)  # ТЕПЕРЬ НУЖНО ЭТУ ОЧЕРЕДЬ ЗАБИНДИТЬ К ТОЧКЕ ОБМЕНА
        self.channel.basic_consume(queue=self.callback_queue,
                                   on_message_callback=self.on_response,
                                   # Данные с сервера приходят сюда,Response пропишем позже
                                   auto_ack=True)  # Данные должны быть уведомлены что пришли

        self.response = None
        self.corr_id = None
        self.token = None
        self.tank_id = None
        self.room_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)
            print(self.response)

    def call(self, key, message={}):  # функция будет отправлять наши запросы на сервер
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='X:routing.topic',
            routing_key=key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(message)  # меняем в json формат
        )
        while self.response is None:
            self.connection.process_data_events()

    def check_server_status(self):  # Чтобы узнать сервер статус
        self.call('tank.request.healthcheck')
        return self.response['status'] == '200'  # если сервер активный то вернет 200

    def obtain_token(self, room_id):
        message = {
            'roomId': room_id
        }
        self.call('tank.request.register', message)
        if 'token' in self.response:
            self.token = self.response['token']
            self.tank_id = self.response['tankId']
            self.room_id = self.response['roomId']
            return True
        return False

    def turn_tank(self, token, direction):
        message = {
            'token': token,
            'direction': direction
        }
        self.call('tank.request.turn', message)


class TankConsumerClient(Thread):

    def __init__(self, room_id):
        super().__init__()
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=IP,
                port=PORT,
                virtual_host=VIRTUAL_HOST,
                credentials=pika.PlainCredentials(
                    username=USERNAME,
                    password=PASSWORD
                )
            )
        )
        self.channel = self.connection.channel()
        queue = self.channel.queue_declare(queue='', exclusive=True, auto_delete=True)
        event_listener = queue.method.queue
        self.channel.queue_bind(exchange='X:routing.topic', queue=event_listener, routing_key='event.state.' + room_id)
        self.channel.basic_consume(
            queue=event_listener,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        self.response = None

    def on_response(self, ch, method, props, body):
        self.response = json.loads(body)
        # print(self.response)

    def run(self):
        self.channel.start_consuming()


UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

MOVE_KEYS = {
    pygame.K_w: UP,
    pygame.K_a: LEFT,
    pygame.K_s: DOWN,
    pygame.K_d: RIGHT
}


def draw_tank(x, y, width, height, direction):
    tank_c = (x + int(width / 2), y + int(width / 2))
    pygame.draw.rect(screen, (255, 0, 0), (x, y, width, width), 2)
    pygame.draw.circle(screen, (255, 0, 0), tank_c, int(width / 2))


def game_start():
    mainloop = True
    font = pygame.font.Font('freesansbold.ttf', 32)
    while mainloop:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False
                if event.key in MOVE_KEYS:
                    client.turn_tank(client.token, MOVE_KEYS[event.key])

        try:
            remaining_time = event_client.response['remainingTime']
            text = font.render('Remaining Time: {}'.format(remaining_time), True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (500, 100)
            screen.blit(text, textRect)
            hits = event_client.response['hits']
            bullets = event_client.response['gameField']['bullets']
            winners = event_client.response['winners']
            tanks = event_client.response['gameField']['tanks']
            for tank in tanks:
                tank_x = tank['x']
                tank_y = tank['y']
                tank_width = tank['width']
                tank_height = tank['height']
                tank_direction = tank['direction']
                draw_tank(tank_x, tank_y, tank_width, tank_height, tank_direction)
        except Exception as e:
            # print(str(e))
            pass
        pygame.display.flip()

    client.connection.close()
    pygame.quit()


client = TankRpcClient()
client.check_server_status()
client.obtain_token('room-5')
event_client = TankConsumerClient('room-5')
event_client.start()
game_start()
