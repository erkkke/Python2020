import pygame
import random
from enum import Enum
from threading import Thread
import pika
import json
import uuid
import math

# pylint: disable=no-member


pygame.init()
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('RoadTo30Points')

grass = pygame.image.load('pic/grass.jpg')
background_multi = pygame.image.load('pic/background_multi.jpg')
tank_img1 = pygame.transform.scale(pygame.image.load('pic/tank_blue1.png'), (30, 50))
tank_img2 = pygame.transform.scale(pygame.image.load('pic/tank_red1.png'), (30, 50))

enemy_tank_multi = pygame.image.load('pic/enemy_tank.png')
player_tank_multi = pygame.image.load('pic/player_tank.png')

life_blue = pygame.image.load('pic/life_blue.png')
life_red = pygame.image.load('pic/life_red.png')

bullet_sound = pygame.mixer.Sound('sound/shoot.mp3')
bullet_sound.set_volume(0.2)
hit_sound = pygame.mixer.Sound('sound/hit.wav')
hit_sound.set_volume(0.5)
wall_explotion = pygame.mixer.Sound('sound/wall_explotion.wav')
wall_explotion.set_volume(0.2)

music = pygame.mixer.music.load('sound/music.wav')


GameOver_single = pygame.image.load('pic/game_over_single.jpg')
AFK_img = pygame.image.load('pic/AFK.png')
wall_img = pygame.transform.scale(pygame.image.load('pic/wall.png'), (32, 32))
bonus_img = pygame.transform.scale(pygame.image.load('pic/bonus.png'), (32, 32))


def background_single(img):
    for i in range(0, 600, 200):
        for j in range(0, 800, 200):
            screen.blit(img, (j, i))


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Tank:

    def __init__(self, x, y, tank_img, life_img, life_img_positions, color, left, right, up, down, fire):
        self.x, self.y = x, y
        self.life_img = life_img
        self.life_img_positions = life_img_positions
        self.life = 5
        self.color = color
        self.speed = 3
        self.bullet_speed = 15
        self.direction = 0
        self.stay = True
        self.image = tank_img
        self.rotate_image = tank_img
        self.fire_key = fire
        self.tap = {right: Direction.RIGHT, left: Direction.LEFT, up: Direction.UP, down: Direction.DOWN}

    def move_and_draw_by_direction(self):
        if not self.stay:

            if self.direction == Direction.UP:
                self.rotate_image = pygame.transform.rotate(self.image, 180)
                self.y -= self.speed
                if self.y < 0:
                    self.y = screen.get_height()

            if self.direction == Direction.DOWN:
                self.rotate_image = pygame.transform.rotate(self.image, 0)
                self.y += self.speed
                if self.y > screen.get_height():
                    self.y = 0

            if self.direction == Direction.LEFT:
                self.rotate_image = pygame.transform.rotate(self.image, -90)
                self.x -= self.speed
                if self.x < 0:
                    self.x = screen.get_width()

            if self.direction == Direction.RIGHT:
                self.rotate_image = pygame.transform.rotate(self.image, 90)
                self.x += self.speed
                if self.x > screen.get_width():
                    self.x = 0

        screen.blit(self.rotate_image, (self.x, self.y))

    def change_direction(self, direction):
        self.direction = direction

    def life_draw(self):
        for i in range(self.life):
            screen.blit(self.life_img, (self.life_img_positions[0] + (26 * i), self.life_img_positions[1]))


class Gun:

    def __init__(self, tank):
        self.speed = tank.bullet_speed
        self.color = tank.color
        self.width, self.height = 0, 0
        self.direction = tank.direction
        self.bullet_distruction_time = 3
        self.bullet_lifetime = 0

        if tank.direction == Direction.UP:
            self.x = tank.x + tank.rotate_image.get_width() // 2
            self.y = tank.y - 10
        if tank.direction == Direction.DOWN:
            self.x = tank.x + tank.rotate_image.get_width() // 2
            self.y = tank.y + tank.rotate_image.get_height() + 10
        if tank.direction == Direction.LEFT:
            self.x = tank.x - 10
            self.y = tank.y + tank.rotate_image.get_width() // 2 - 13
        if self.direction == Direction.RIGHT:
            self.x = tank.x + tank.rotate_image.get_height() + 10
            self.y = tank.y + tank.rotate_image.get_height() // 2

    def move(self, seconds):
        self.bullet_lifetime += seconds


        if self.direction == Direction.UP:
            self.width, self.height = 5, 10
            self.y -= self.speed

        if self.direction == Direction.DOWN:
            self.width, self.height = 5, 10
            self.y += self.speed

        if self.direction == Direction.LEFT:
            self.width, self.height = 10, 5
            self.x -= self.speed

        if self.direction == Direction.RIGHT:
            self.width, self.height = 10, 5
            self.x += self.speed

        pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.width, self.height))


def game_over_single_scene(tanks):
    if tanks[0].life <= 0: won = 'RED team won'
    elif tanks[1].life <= 0: won = 'BLUE team won'
    font = pygame.font.SysFont('comicsansms', 35, 1)
    font2 = pygame.font.SysFont('comicsansms', 20, 1)

    text = font.render(won, 1, (0, 255, 0))
    textRect = text.get_rect()
    textRect.center = (400, 340)

    text2 = font2.render('Press R to go back to menu', 1, (200, 200, 200))
    text2Rect = text2.get_rect()
    text2Rect.center = (400, 395)

    screen.blit(GameOver_single, (0, 0))
    screen.blit(text, textRect)
    screen.blit(text2, text2Rect)

class Wall:
    def __init__(self, coordinates):
        self.size = wall_img.get_width()
        self.x = coordinates[0] * self.size
        self.y = coordinates[1] * self.size
        self.image = wall_img

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class Collisions:

    def __init__(self):
        self.end = 10.0
        self.slowdown_end = 5.0
        self.isSuper = False
        self.time = 0.0

    def wall_and_tank(self, tanks, walls, sec):
        for wall in walls:
            for tank in tanks:

                self.x = wall.x - tank.x
                self.y = wall.y - tank.y

                if -wall.size <= self.x <= tank.rotate_image.get_width() and -wall.size <= self.y <= \
                        tank.rotate_image.get_height():
                    walls.remove(wall)
                    tank.life -= 1
                    wall_explotion.play()

    def wall_and_bullet(self, bullets, walls):
        for wall in walls:
            for bullet in bullets:
                self.x = wall.x - bullet.x
                self.y = wall.y - bullet.y

                if -wall.size <= self.x <= bullet.width and -wall.size <= self.y <= bullet.height:
                    bullets.remove(bullet)
                    walls.remove(wall)
                    wall_explotion.play()

    def tank_and_bullet(self, tanks, bullets):
        for tank in tanks:
            for bullet in bullets:
                self.x = bullet.x - tank.x
                self.y = bullet.y - tank.y

                if -bullet.width <= self.x <= tank.rotate_image.get_width() and -bullet.height <= self.y <= \
                        tank.rotate_image.get_height():
                    bullets.remove(bullet)
                    tank.life -= 1
                    hit_sound.play()

    def tank_and_bonus(self, tank, bonus):
            self.x = tank.x - bonus.coordinates[0]
            self.y = tank.y - bonus.coordinates[1]

            if -tank.rotate_image.get_width() <= self.x <= bonus.size and -tank.rotate_image.get_height() <= self.y \
                    <= bonus.size and bonus.isBonus:
                bonus.isBonus = False
                return True
            return False


class Bonus:
    def __init__(self):
        self.image = bonus_img
        self.size = bonus_img.get_width()
        self.isBonus = False
        self.wait = 0
        self.reload = 5
        self.coordinates = random.choice(Map().bonus_spawnpoints)

    def new_bonus(self):
        self.reload = random.randrange(5, 12)
        self.coordinates = random.choice(Map().bonus_spawnpoints)

    def draw(self):
        screen.blit(self.image, self.coordinates)


class Map:

    def __init__(self):
        global maps
        self.y = 0
        self.walls = []
        self.bonus_spawnpoints = []
        self.tank_spawnpoints = []

        self.walls.clear()
        self.bonus_spawnpoints.clear()
        self.tank_spawnpoints.clear()

        with open(random.choice(maps)) as map:
            lines = map.readlines()
            for row in lines:
                self.x = 0
                for col in row:
                    if col == '#':
                        self.walls.append(Wall([self.x, self.y]))
                    elif col == '1':
                        self.bonus_spawnpoints.append([self.x * 32, self.y * 32])
                    elif col == '0':
                        self.tank_spawnpoints.append([self.x * 32, self.y * 32])
                    self.x += 1
                self.y += 1


def single_game_run():
    global clock, FPS, bullets, tanks, isGameOver, restart
    map = Map()
    bonus = Bonus()
    tank1 = Tank(map.tank_spawnpoints[0][0], map.tank_spawnpoints[0][1], tank_img1, life_blue, (20, 20), (50, 50, 255),
                 pygame.K_a,
                 pygame.K_d,
                 pygame.K_w,
                 pygame.K_s,
                 pygame.K_SPACE)
    tank2 = Tank(map.tank_spawnpoints[1][0], map.tank_spawnpoints[1][1], tank_img2, life_red, (650, 20), (220, 5, 5),
                 pygame.K_LEFT,
                 pygame.K_RIGHT, pygame.K_UP,
                 pygame.K_DOWN, pygame.K_RETURN)

    tanks = [tank1, tank2]
    collision = Collisions()

    mainloop = True

    while mainloop:

        millis = clock.tick(FPS)
        seconds = millis / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    mainloop = False
                    restart = True

                for tank in tanks:
                    if event.key == tank.fire_key:

                        bullets.append(Gun(tank))
                        bullet_sound.play()

        pressed = pygame.key.get_pressed()

        for tank in tanks:
            stay = False
            for key in tank.tap.keys():
                if pressed[key]:
                    stay = False
                    tank.change_direction(tank.tap[key])

            if stay:
                tank.stay = True
            else:
                tank.stay = False

        for tank in tanks:
            if tank.life == 0:
                isGameOver = True
                game_over_single_scene(tanks)
                if pressed[pygame.K_r]:
                    mainloop = False
                    restart = True

        if not isGameOver:
            background_single(grass)
            for bullet in bullets:
                bullet.move(seconds)

            for bullet in bullets:
                if bullet.bullet_lifetime >= bullet.bullet_distruction_time:
                    bullets.remove(bullet)

            for wall in map.walls:
                wall.draw()

            if bonus.isBonus:
                bonus.draw()
            elif bonus.wait < bonus.reload:
                bonus.wait += seconds
            else:
                bonus.new_bonus()
                bonus.wait = 0
                bonus.isBonus = True

            collision.tank_and_bullet(tanks, bullets)
            collision.wall_and_tank(tanks, map.walls, seconds)
            collision.wall_and_bullet(bullets, map.walls)

            for tank in tanks:
                if collision.tank_and_bonus(tank, bonus):
                    collision.isSuper = True
                    tank.speed = 5
                    tank.bullet_speed = 25
                if collision.isSuper and collision.time <= collision.end:
                    collision.time += seconds
                else:
                    collision.isSuper = False
                    collision.time = 0.0
                    tank.speed = 3
                    tank.bullet_speed = 15

            for tank in tanks:
                tank.move_and_draw_by_direction()
                tank.life_draw()

        pygame.display.update()




#_______________________________________ Client Connection _______________________________________________


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
        # print(self.response)

    def run(self):
        self.channel.start_consuming()




#_______________________________ MULTIPLAYER FUNCTIONS _________________________________


def draw_tank(tank_id, x, y, size, direction):
    global enemy_tank_multi, player_tank_multi
    image = enemy_tank_multi if tank_id != client.tank_id else player_tank_multi
    rotate_image = image
    tank_center = (x + size // 2, y + size // 2)
    nickname_font = pygame.font.SysFont('monaco', 20)
    nickname_color = (0, 0, 0)
    if client.tank_id == tank_id: nickname = 'you'
    else: nickname = tank_id

    if direction == 'UP':
        rotate_image = image
    elif direction == 'DOWN':
        rotate_image = pygame.transform.rotate(image, 180)
    elif direction == 'LEFT':
        rotate_image = pygame.transform.rotate(image, 90)
    elif direction == 'RIGHT':
        rotate_image = pygame.transform.rotate(image, -90)

    screen.blit(rotate_image, (x, y))
    nick = nickname_font.render(nickname, True, nickname_color)
    nickRect = nick.get_rect()
    nickRect.center = (tank_center[0], tank_center[1] + 25)
    screen.blit(nick, nickRect)


def draw_bullet(owner, x, y, width, height):
    mycolor = (0, 204, 102)
    enemycolor = (176, 0, 0)

    if client.tank_id == owner:
        pygame.draw.ellipse(screen, mycolor, (x, y, width, height))
    else:
        pygame.draw.ellipse(screen, enemycolor, (x, y, width, height))

    pygame.draw.ellipse(screen, (50, 50, 50), (x, y, width, height), 1)


def kicked_scene(score):
    global restart

    kickedfont = pygame.font.SysFont('comicsansms', 20, True)

    Restart = Button('Restart', 175, 450, 150, 40, (0, 100, 0), (0, 176, 0), None)
    Quit = Button('Quit', 500, 450, 150, 40, (100, 0, 0), (176, 0, 0), None)
    buttons = [Restart, Quit]
    action = ''

    color = (0, 0, 0)

    text = kickedfont.render('You have been kicked for 30 seconds AFK', True, color)
    score_text = kickedfont.render(f'Your score: {score}', 1, color)

    textRect = text.get_rect()
    textRect.center = (400, 290)
    score_textRect = score_text.get_rect()
    score_textRect.center = (400, 330)

    message3 = kickedfont.render('Press ESC to go back to menu', 1, (70, 70, 70))
    message3Rect = message3.get_rect()
    message3Rect.center = (400, 50)

    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show = False
                    restart = True

            mouse = pygame.mouse.get_pos()

            for button in buttons:
                if button.x <= mouse[0] <= button.x + button.width and button.y <= mouse[1] <= button.y + button.height:
                    button.isActive = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        action = button.text
                        show = False
                else: button.isActive = False

        screen.fill((255, 255, 255))
        screen.blit(AFK_img, (545, 20))
        screen.blit(text, textRect)
        screen.blit(score_text, score_textRect)
        screen.blit(message3, message3Rect)

        for button in buttons:
            button.draw()

        pygame.display.update()

    if action == 'Restart': multiplayer_game_start()
    elif action == 'Quit': quit()


def game_over_scene(whoiam, score):
    global restart
    font1 = pygame.font.SysFont('comicsansms', 30)
    font2 = pygame.font.SysFont('comicsansms', 20)
    Restart = Button('Restart', 175, 450, 150, 40, (0, 100, 0), (0, 176, 0), None)
    Quit = Button('Quit', 500, 450, 150, 40, (100, 0, 0), (176, 0, 0), None)
    buttons = [Restart, Quit]
    action = ''

    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show = False
                    restart = True

            mouse = pygame.mouse.get_pos()

            for button in buttons:
                if button.x <= mouse[0] <= button.x + button.width and button.y <= mouse[1] <= button.y + button.height:
                    button.isActive = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        action = button.text
                        show = False
                else: button.isActive = False

        if whoiam == 'winner':
            # color = (0, 170, 0)
            text = 'You won!'
        else:
            # color = (170, 0, 0)
            text = 'You lost, lucky next time!'

        message1 = font1.render(text, 1, (255, 255, 255))
        message1Rect = message1.get_rect()
        message1Rect.center = (400, 340)

        message2 = font1.render(f'Your score: {score}', 1, (255, 255, 255))
        message2Rect = message2.get_rect()
        message2Rect.center = (400, 390)

        message3 = font2.render('Press ESC to go back to menu', 1, (150, 150, 150))
        message3Rect = message3.get_rect()
        message3Rect.center = (400, 50)

        screen.blit(GameOver_single, (0, 0))
        screen.blit(message1, message1Rect)
        screen.blit(message2, message2Rect)
        screen.blit(message3, message3Rect)

        for button in buttons:
            button.draw()

        pygame.display.update()

    if action == 'Restart': multiplayer_game_start()
    elif action == 'Quit': quit()




#________________________________ MULTIPLAYER _______________________________


def multiplayer_game_start():
    global restart, screen, bullet_sound, hit_sound, whoiam, myscore, room

    screen = pygame.display.set_mode((1000, 600))
    moving_keys = {pygame.K_w: 'UP', pygame.K_s: 'DOWN', pygame.K_a: 'LEFT', pygame.K_d: 'RIGHT'}
    isKicked = False
    game_over = False

    sound = 0

    client.check_server_status()
    client.register(room)
    event_client = Consumer_client(client.room_id)
    event_client.start()

    font = pygame.font.SysFont('comicsansms', 16)
    info_panel_font = pygame.font.SysFont('monaco', 20)

    mainloop = True
    while mainloop:

        screen.fill((255, 250, 222))
        screen.blit(background_multi, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.connection.close()
                event_client.channel.stop_consuming()
                quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    mainloop = False
                    restart = True

                if event.key in moving_keys:
                    client.turn_tank(client.token, moving_keys[event.key])

                if event.key == pygame.K_SPACE:
                    client.fire(client.token)

        try:
            tanks = event_client.response['gameField']['tanks']
            bullets = event_client.response['gameField']['bullets']

            for bullet in bullets:
                bullet_owner = bullet['owner']
                bullet_x, bullet_y = bullet['x'], bullet['y']
                bullet_width, bullet_height = bullet['width'], bullet['height']
                draw_bullet(bullet_owner, bullet_x, bullet_y, bullet_width, bullet_height)

            for tank in tanks:
                tank_x, tank_y = tank['x'], tank['y']
                tank_id = tank['id']
                tank_size = tank['width']
                tank_direction = tank['direction']
                draw_tank(tank_id, tank_x, tank_y, tank_size, tank_direction)


            score = {tank['id']: [tank['score'], tank['health']] for tank in tanks}
            sorted_score = sorted(score.items(), key=lambda kv: kv[1], reverse=True)
            i = 100
            for x in sorted_score:
                if x[0] == client.tank_id: color = (0, 153, 20)
                else: color = (176, 0, 0)
                health_score = font.render(x[0] + ':    ' + str(x[1][0]) + '    ' +
                                                              str(x[1][1]), True, color)
                health_scoreRect = health_score.get_rect()
                health_scoreRect.center = (920, i)
                screen.blit(health_score, health_scoreRect)
                i += 30


            if sound < len(bullets): bullet_sound.play()
            sound = len(bullets)

            if event_client.response['hits']: hit_sound.play()



        except: pass

        try:
            remaining_time = event_client.response['remainingTime']
            text = font.render(f'Remaining Time: {remaining_time}', True, (30, 30, 30))
            textRect = text.get_rect()
            textRect.center = (400, 40)
            screen.blit(text, textRect)
        except: pass

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


        if event_client.response['kicked']:
            kicked = event_client.response['kicked']
            for kick in kicked:
                if kick['tankId'] == client.tank_id:
                    mainloop = False
                    myscore = kick['score']
                    isKicked = True

        if event_client.response['winners']:
            winners = event_client.response['winners']
            for winner in winners:
                if winner['tankId'] == client.tank_id:
                    mainloop = False
                    game_over = True
                    whoiam = 'winner'
                    myscore = winner['score']

        if event_client.response['losers']:
            losers = event_client.response['losers']
            for loser in losers:
                if loser['tankId'] == client.tank_id:
                    mainloop = False
                    game_over = True
                    whoiam = 'loser'
                    myscore = loser['score']

        tanks = event_client.response['gameField']['tanks']
        winners = event_client.response['winners']
        losers = event_client.response['losers']

        if len(tanks) == 0:
            mainloop = False
            game_over = True
            for winner in winners:
                if winner['tankId'] == client.tank_id:
                    whoiam = 'winner'
                    myscore = winner['score']
            for loser in losers:
                if loser['tankId'] == client.tank_id:
                    whoiam = 'loser'
                    myscore = loser['score']

        pygame.display.update()

    screen = pygame.display.set_mode((800, 600))
    event_client.channel.stop_consuming()
    if game_over:
        game_over_scene(whoiam, myscore)
    elif isKicked:
        kicked_scene(myscore)




#_____________________________________ AI _______________________________________________


def turn(direction):
    client.turn_tank(client.token, direction)

def fire():
    client.fire(client.token)
    return True

def random_direction(tank, mytank):
    global move
    if tank['direction'] == mytank['direction']:
        direction = random.choice(move)
        if direction != mytank['direction']: client.turn_tank(client.token, direction)


def AI_game_start():
    global restart, screen, bullet_sound, hit_sound, whoiam, myscore, mytank, up, down, left, right, room

    screen = pygame.display.set_mode((1000, 600))

    isKicked = False
    game_over = False

    sound = 0

    client.check_server_status()
    client.register(room)
    event_client = Consumer_client(client.room_id)
    event_client.start()

    font = pygame.font.SysFont('comicsansms', 16)
    info_panel_font = pygame.font.SysFont('monaco', 20)
    turn(up)

    mainloop = True
    while mainloop:
        screen.fill((255, 250, 222))
        screen.blit(background_multi, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.connection.close()
                event_client.channel.stop_consuming()
                quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    mainloop = False
                    restart = True
        tanks = event_client.response['gameField']['tanks']
        bullets = event_client.response['gameField']['bullets']
        remaining_time = event_client.response['remainingTime']

        try:
            isFire = False
            isHide = False

            mybullet = []

            for tank in tanks:
                if tank['id'] == client.tank_id:
                    mytank = tank

            for bullet in bullets:
                bullet_owner = bullet['owner']
                bullet_x, bullet_y = bullet['x'], bullet['y']
                bullet_width, bullet_height = bullet['width'], bullet['height']
                if bullet['owner'] == client.tank_id:
                    mybullet.append(bullet)
                draw_bullet(bullet_owner, bullet_x, bullet_y, bullet_width, bullet_height)

            for tank in tanks:
                tank_x, tank_y = tank['x'], tank['y']
                tank_id = tank['id']
                tank_size = tank['width']
                tank_direction = tank['direction']
                if tank['id'] == client.tank_id:
                    mytank = tank
                draw_tank(tank_id, tank_x, tank_y, tank_size, tank_direction)

            target = tanks[0] if tanks[0]['id'] != mytank['id'] else tanks[1]




            if len(tanks) >= 2:
                if remaining_time % 5 == 0 and (remaining_time // 5) % 2 == 0: turn(right)
                elif remaining_time % 5 == 0 and (remaining_time // 5) % 2 != 0: turn(up)
                if not isHide:
                    for tank in tanks:
                        if tank['id'] != mytank['id']:
                            if tank['y'] + 30 >= mytank['y'] >= tank['y'] - 15:
                                if mytank['x'] < tank['x']: turn(right)
                                else: turn(left)
                                if fire():
                                    turn(up)
                                    isFire = True

                            elif tank['x'] + 30 >= mytank['x'] >= tank['x'] - 15:
                                if mytank['y'] < tank['y']: turn(down)
                                else: turn(up)
                                if fire():
                                    turn(left)
                                    isFire = True

                        # elif math.sqrt((target['x'] - mytank['x'] + 31)**2 + (target['y'] - mytank['y'] + 31)**2) > 100:
                        #     if target['direction'] == up or target['direction'] == down:
                        #         if target['x'] > mytank['x'] + 31:
                        #             turn(right)
                        #         else:
                        #             turn(left)
                        #     elif target['direction'] == left or target['direction'] == right:
                        #         if target['y'] > mytank['y'] + 31:
                        #             turn(down)
                        #         else:
                        #             turn(up)

                        # else:
                        #     if mytank['x'] + 32 < target['x'] or mytank['x'] > target['x'] + 32:
                        #         if target['direction'] == up:
                        #                 turn(down)
                        #         elif target['direction'] == down:
                        #             turn(up)
                        #     if mytank['y'] + 32 < target['y'] or mytank['y'] > target['y'] + 32:
                        #         if target['direction'] == left: turn(right)
                        #         elif target['direction'] == right: turn(left)

                if not isFire:
                    for bullet in bullets:
                        if bullet['owner'] != mytank['id']:
                            if bullet['y'] + 5 >= mytank['y'] and bullet['y'] <= mytank['y'] + 31:
                                if bullet['x'] < mytank['x'] and bullet['direction'] == 'RIGHT': turn(up)
                                elif bullet['x'] > mytank['x'] and bullet['direction'] == 'LEFT': turn(up)

                            elif bullet['x'] + 5 >= mytank['x'] and bullet['x'] <= mytank['x'] + 31:
                                if bullet['y'] < mytank['y'] and bullet['direction'] == 'DOWN': turn(left)
                                elif bullet['y'] > mytank['y'] and bullet['direction'] == 'UP': turn(left)


            if sound < len(bullets): bullet_sound.play()
            sound = len(bullets)

            if event_client.response['hits']: hit_sound.play()
        except: pass

        try:
            remaining_time = event_client.response['remainingTime']
            text = font.render(f'Remaining Time: {remaining_time}', True, (30, 30, 30))
            textRect = text.get_rect()
            textRect.center = (400, 40)
            screen.blit(text, textRect)
        except:
            pass

        if len(tanks) == 1:
            if remaining_time % 5 == 0 and (remaining_time // 5) % 2 == 0:
                turn(right)
            elif remaining_time % 5 == 0 and (remaining_time // 5) % 2 != 0:
                turn(up)

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

        score = {tank['id']: [tank['score'], tank['health']] for tank in tanks}
        sorted_score = sorted(score.items(), key=lambda kv: kv[1], reverse=True)
        i = 100
        for x in sorted_score:
            if x[0] == client.tank_id:
                color = (0, 153, 20)
            else:
                color = (176, 0, 0)
            health_score = font.render(x[0] + ':    ' + str(x[1][0]) + '    ' +
                                       str(x[1][1]), True, color)
            health_scoreRect = health_score.get_rect()
            health_scoreRect.center = (920, i)
            screen.blit(health_score, health_scoreRect)
            i += 30

        losers = event_client.response['losers']
        winners = event_client.response['winners']

        if event_client.response['kicked']:
            kicked = event_client.response['kicked']
            for kick in kicked:
                if kick['tankId'] == client.tank_id:
                    mainloop = False
                    myscore = kick['score']
                    isKicked = True

        if winners:
            for winner in winners:
                if winner['tankId'] == client.tank_id:
                    whoiam = 'winner'
                    myscore = winner['score']
            mainloop = False
            game_over = True

        if losers:
            for loser in losers:
                if loser['tankId'] == client.tank_id:
                    whoiam = 'loser'
                    myscore = loser['score']
                    mainloop = False
                    game_over = True

        if len(tanks) == 0:
            mainloop = False
            game_over = True
            for winner in winners:
                if winner['tankId'] == client.tank_id:
                    whoiam = 'winner'
                    myscore = winner['score']
            for loser in losers:
                if loser['tankId'] == client.tank_id:
                    whoiam = 'loser'
                    myscore = loser['score']





        pygame.display.update()

    screen = pygame.display.set_mode((800, 600))
    event_client.channel.stop_consuming()
    if game_over:
        game_over_scene(whoiam, myscore)
    elif isKicked:
        kicked_scene(myscore)




#_____________________________________ MENU _____________________________________________


class Button:
    def __init__(self, text, x, y, width, height, active_colour, nonactive_colour, font=None):
        self.isActive = False
        self.active_colour = active_colour
        self.nonactive_colour = nonactive_colour
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.text = text

        self.font = pygame.font.SysFont('comicssansms', 25) if font==None else font
        self.message = self.font.render(str(text), 1, (0, 0, 0))

        txt_w, txt_h = self.message.get_size()
        self.txt_x = x + width // 2 - txt_w // 2
        self.txt_y = y + height // 2 - txt_h // 2

    def draw(self):
        color = self.active_colour if self.isActive else self.nonactive_colour

        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), 1)
        screen.blit(self.message, (self.txt_x, self.txt_y))


def show_menu():
    global game_mode
    menu_background = pygame.transform.scale(pygame.image.load('pic/menu.jpg'), (800, 600))

    single_button = Button('Single Play', 100, 350, 150, 30, (255, 178, 102), (153, 255, 255))
    multiplay_button = Button('Multiplayer', 100, 400, 150, 30, (255, 178, 102), (153, 255, 255))
    ai_button = Button('AI mode', 100, 450, 150, 30, (255, 178, 102), (153, 255, 255))

    buttons = [single_button, multiplay_button, ai_button]

    show = True

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show = False

            mouse = pygame.mouse.get_pos()

            for button in buttons:
                if button.x <= mouse[0] <= button.x + button.width and button.y <= mouse[1] <= button.y + button.height:
                    button.isActive = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        game_mode = button.text
                        show = False
                else: button.isActive = False

        screen.blit(menu_background, (0, 0))

        for button in buttons:
            button.draw()

        pygame.display.update()



#------------------------------ MAIN -------------------------------------

isGameOver = False
restart = True

maps = ['pic/map.txt', 'pic/map2.txt']
bullets = []
tanks = []
walls = []
bonus_spawnpoints = []
tank_spawnpoints = []
clock = pygame.time.Clock()
FPS = 25
whoiam = ''
myscore = 0
game_mode = ''
mytank = []
room = 'room-14'

up = 'UP'
down = 'DOWN'
left = 'LEFT'
right = 'RIGHT'
move = [up, down, left, right]

ip = '34.254.177.17'
port = 5672
virtual_host = 'dar-tanks'
username = 'dar-tanks'
password = '5orPLExUYnyVYZg48caMpX'

client = RPC_client()

while restart:
    restart = False
    isGameOver = False
    whoiam = ''
    myscore = 0
    mytank = []
    bullets = []
    tanks = []
    game_mode = ''
    show_menu()
    if game_mode == 'Single Play': single_game_run()
    elif game_mode == 'Multiplayer': multiplayer_game_start()
    elif game_mode == 'AI mode': AI_game_start()

pygame.quit()