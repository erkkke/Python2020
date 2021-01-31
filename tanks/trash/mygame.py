import pygame
import random
from enum import Enum
#pylint: disable=no-member

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Tanks')
grass = pygame.image.load('pic/grass.jpg')

tank_img1 = pygame.transform.scale(pygame.image.load('pic/tank_blue1.png'), (40, 60))
tank_img2 = pygame.transform.scale(pygame.image.load('pic/tank_red1.png'), (40, 60))

life_blue = pygame.image.load('pic/life_blue.png')
life_red = pygame.image.load('pic/life_red.png')

bullet_sound = pygame.mixer.Sound('sound/shoot.mp3')
hit_sound = pygame.mixer.Sound('sound/hit.wav')

pygame.mixer.music.load('sound/music.wav')

GameOver_background = pygame.transform.scale(pygame.image.load('pic/background2.jpg'), (200, 200))


def background(background):
    for i in range(0, 600, 200):
        for j in range(0, 800, 200):
            screen.blit(grass, (j, i))

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
        self.life = 3
        self.color = color
        self.speed = 3
        self.direction = 0
        self.stay = True
        self.image = tank_img
        self.rotate_image = tank_img
        self.fire_key = fire
        self.tap = {right : Direction.RIGHT, left : Direction.LEFT, up : Direction.UP, down : Direction.DOWN}

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
                self.rotate_image = pygame.transform.rotate(self.image, 270)
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
        self.speed = 15
        self.color = tank.color
        self.width , self.height = 0, 0
        self.direction = tank.direction
        self.bullet_distruction_time = 1
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
            self.width , self.height = 5, 10
            self.y -= self.speed
            # if self.y <= 0:
            #     self.y = 600
            
        if self.direction == Direction.DOWN:
            self.width , self.height = 5, 10
            self.y += self.speed
            # if self.y >= 600:
            #     self.y = 0
            
        if self.direction == Direction.LEFT:
            self.width, self.height = 10, 5
            self.x -= self.speed
            # if self.x <= 0:
            #     self.x = 800

        if self.direction == Direction.RIGHT:
            self.width, self.height = 10, 5
            self.x += self.speed
            # if self.x >= 800:
            #     self.x = 0

        pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.width, self.height))


class GameOver_scene:
    def __init__(self):
        global GameOver_background
        for i in range(0, 600, 200):
            for j in range(0, 800, 200):
                screen.blit(GameOver_background, (j, i))


    def titles(self, tanks):
        if tanks[0].life <= 0: self.won = 'RED team won'
        if tanks[1].life <= 0: self.won = 'BLUE team won'
        self.font = pygame.font.SysFont('comicsansms', 50, 1)
        self.text1 = self.font.render('GAME OVER', 1, (50, 205, 50))
        self.text2 = self.font.render(self.won, 1, (50, 205, 50))
        screen.blit(self.text1, ((screen.get_width() - self.text1.get_width()) // 2 + 40, screen.get_height() // 2 - self.text1.get_height()))
        screen.blit(self.text2, ((screen.get_width() - self.text1.get_width()) // 2, screen.get_height() // 2))
    
        

def collision(tank, bullet):
    x = bullet.x - tank.x
    y = bullet.y - tank.y
    if -bullet.width <= x <= tank.rotate_image.get_width() and -bullet.height <= y <= tank.rotate_image.get_height():
        return True
    return False

      
tank1 = Tank(50, 50, tank_img1, life_blue, (20, 20), (50, 50, 255), pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE)
tank2 = Tank(700, 500, tank_img2, life_red, (705, 20), (220, 5, 5), pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN)
tanks = [tank1, tank2]
bullets = []
isGameOver = False

clock = pygame.time.Clock()
FPS = 25


while True:
    millis = clock.tick(FPS)
    seconds = millis / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_ESCAPE:
                quit()

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

        if stay: tank.stay = True
        else: tank.stay = False
    
    for tank in tanks:
        if tank.life == 0:
            isGameOver = True
            GameOver_scene().titles(tanks)
    
    if not isGameOver:
        background(grass)
        for bullet in bullets:
            bullet.move(seconds)
        
        for tank in tanks:
            for bullet in bullets:
                isCollision = False
                if collision(tank, bullet):
                    isCollision = True
                    bullets.remove(bullet)
                    
                if bullet.bullet_lifetime >= bullet.bullet_distruction_time:
                    bullets.remove(bullet)

                if isCollision:
                    tank.life -= 1
                    hit_sound.play()



        for tank in tanks:
            tank.move_and_draw_by_direction()
            tank.life_draw()

    pygame.display.flip()

pygame.quit()