import pygame
from threading import Thread
import pika
import json
import uuid
import sys
from operator import itemgetter
# pylint: disable=no-member


pygame.init()

ip = '34.254.177.17'
port = 5672
virtual_host = 'dar-tanks'
username = 'dar-tanks'
password = '5orPLExUYnyVYZg48caMpX'

class RPC_client:
    def __init__(self):
        self.credentials = pika.PlainCredentials(username=username, password=password)
        self.parameters = pika.ConnectionParameters(host=ip, port=port, virtual_host=virtual_host, credentials=self.credentials)
        self.connection = pika.BlockingConnection(parameters=self.parameters)

        self.channel = self.connection.channel()

        queue = self.channel.queue_declare(queue='', exclusive=True, auto_delete=True)
        self.callback_queue = queue.method.queue
        self.channel.queue_bind(exchange='X:routing.topic', queue=self.callback_queue)

        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_response, auto_ack=True)

        self.response = None
        self.corr_id = None
        self.token = None
        self.tank_id = None
        self.room_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)
            # print(self.response)

    def call(self, routing_key, message=''):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(
            exchange='X:routing.topic',
            routing_key=routing_key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id),
            body=json.dumps(message))

        while self.response is None:
            self.connection.process_data_events()

    def check_server_status(self):
        self.call('tank.request.healthcheck')
        return self.response['status'] == '200'

    def register(self, room_id):
        message = {'roomId': room_id}
        self.call('tank.request.register', message)

        if 'token' in self.response:
            self.room_id = self.response['roomId']
            self.tank_id = self.response['tankId']
            self.token = self.response['token']

    def turn_tank(self, token, direction):
        message = {
            'token': token,
            'direction': direction
        }
        self.call('tank.request.turn', message)

    def fire(self, token):
        message = {'token': token}
        self.call('tank.request.fire', message)


class Consumer_client(Thread):

    def __init__(self, room_id):
        super().__init__()
        self.credentials = pika.PlainCredentials(username=username, password=password)
        self.parameters = pika.ConnectionParameters(host=ip, port=port, virtual_host=virtual_host,
                                                    credentials=self.credentials)
        self.connection = pika.BlockingConnection(parameters=self.parameters)

        self.channel = self.connection.channel()
        queue = self.channel.queue_declare(queue='', exclusive=True, auto_delete=True)
        event_listener = queue.method.queue
        self.channel.queue_bind(exchange='X:routing.topic',
                                queue=event_listener, routing_key='event.state.'+room_id)

        self.channel.basic_consume(queue=event_listener, on_message_callback=self.on_response, auto_ack=True)

        self.response = None

    def on_response(self, ch, method, props, body):
        self.response = json.loads(body)
        print(self.response)

    def run(self):
        self.channel.start_consuming()


def draw_tank(tank_id, x, y, size, direction):

    tank_center = (x + size // 2, y + size // 2)
    nickname_font = pygame.font.SysFont('monaco', 20)
    nickname_color = (50, 50, 50)
    if client.tank_id == tank_id:
        maincolor = (0, 153, 0)
        color = (0, 204, 102)
        nickname = 'you'
    else:
        maincolor = (102, 0, 204)
        color = (154, 132,245)
        nickname = tank_id

    pygame.draw.rect(screen, maincolor, (x, y, size, size,))
    pygame.draw.circle(screen, color, tank_center, size // 2 - 3)
    if direction == 'UP':
        pygame.draw.line(screen, color, tank_center, (tank_center[0], tank_center[1] - size), 4)
    elif direction == 'DOWN':
        pygame.draw.line(screen, color, tank_center, (tank_center[0], tank_center[1] + size), 4)
    elif direction == 'LEFT':
        pygame.draw.line(screen, color, tank_center, (tank_center[0] - size, tank_center[1]), 4)
    elif direction == 'RIGHT':
        pygame.draw.line(screen, color, tank_center, (tank_center[0] + size, tank_center[1]), 4)

    nick = nickname_font.render(nickname, True, nickname_color)
    nickRect = nick.get_rect()
    nickRect.center = (tank_center[0], tank_center[1] + 25)
    screen.blit(nick, nickRect)




def draw_bullet(owner, x, y, width, height):
    mycolor = (0, 204, 102)
    enemycolor = (154, 132 ,245)

    if client.tank_id == owner:
        pygame.draw.ellipse(screen, mycolor, (x, y, width, height))
    else:
        pygame.draw.ellipse(screen, enemycolor, (x, y, width, height))




screen = pygame.display.set_mode((1000, 600))

def multiplayer_game_start():

    moving_keys = {pygame.K_UP: 'UP', pygame.K_DOWN: 'DOWN', pygame.K_LEFT: 'LEFT', pygame.K_RIGHT: 'RIGHT'}
    room = 'room-3'

    client.check_server_status()
    client.register(room)
    event_client = Consumer_client(client.room_id)
    event_client.start()

    font = pygame.font.SysFont('comicsansms', 16)
    info_panel_font = pygame.font.SysFont('monaco', 20)

    mainloop = True
    while mainloop:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    mainloop = False

                if event.key in moving_keys:
                    client.turn_tank(client.token, moving_keys[event.key])

                if event.key == pygame.K_SPACE:
                    client.fire(client.token)

        try:

            tanks = event_client.response['gameField']['tanks']
            bullets = event_client.response['gameField']['bullets']
            i = 100
            for tank in tanks:
                tank_x, tank_y = tank['x'], tank['y']
                tank_id = tank['id']
                tank_size = tank['width']
                tank_direction = tank['direction']
                draw_tank(tank_id, tank_x, tank_y, tank_size, tank_direction)
            scores = {}
            scores = {tank['id']: [tank['score'], tank['health']] for tank in tanks}
            sorted_scores = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
            for score in sorted_scores:
                if score[0] == client.tank_id: color = (0, 153, 20)
                else: color = (102, 0, 204)

                health_score = font.render(score[0] + ':' + '    ' + str(score[1][0]) + '    ' +
                                                          str(score[1][1]), True, color)

                health_scoreRect = health_score.get_rect()
                health_scoreRect.center = (920, i)
                screen.blit(health_score, health_scoreRect)
                i += 30

            for bullet in bullets:
                bullet_owner = bullet['owner']
                bullet_x, bullet_y = bullet['x'], bullet['y']
                bullet_width, bullet_height = bullet['width'], bullet['height']
                draw_bullet(bullet_owner, bullet_x, bullet_y, bullet_width, bullet_height)
        except:
            pass


        remaining_time = event_client.response['remainingTime']
        text = font.render(f'Remaining Time: {remaining_time}', True, (30, 30, 30))
        textRect = text.get_rect()
        textRect.center = (400, 40)
        screen.blit(text, textRect)



        pygame.draw.line(screen, (0, 0, 0), (840, 0), (840, 800), 2)
        pygame.draw.line(screen, (0, 0, 0), (840, 40), (1000, 40), 2)
        info_panel = info_panel_font.render('INFORMATION PANEL', True, (30, 30, 30))
        textRect = info_panel.get_rect()
        textRect.center = (920, 20)
        screen.blit(info_panel, textRect)

        score_health = info_panel_font.render('SCORE & HEALTH', True, (30, 30, 30))
        score_healthRect = score_health.get_rect()
        score_healthRect.center = (920, 60)
        screen.blit(score_health, score_healthRect)

        pygame.display.flip()


    client.connection.close()
    event_client.channel.stop_consuming()
    pygame.quit()



client = RPC_client()

multiplayer_game_start()