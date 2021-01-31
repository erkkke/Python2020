import pygame
import random

screen = pygame.display.set_mode((800, 600))

def wildPainting():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(o, 255)
    x = random.randint(0, screen.get_size()[0])
    y = random.randint(0, screen.get_size()[1])
    R = random.randint(50, 500)

    pygame.draw.circle(screen, (r, g, b), (x, y), R)

ballx = 300
bally = 300
dx = 50
dy = 50
def draw_ball():
    global ballx, bally, dx, dy
    pygame.draw.circle(screen, (255, 0, 0), (ballx, bally), 10)
    ballx += dx
    bally += dy
    if ballx + 2 * 10 > screen.get_size()[0] or ballx < 0:
        dx += -1
    if bally + 2 *10 > screen.get_size()[1] or bally < 0:
        dy += -1


fps = 30

clock = pygame.time.Clock()

while True:
    millis = clock.tick(fps)
    for event in pygame.event.get:
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
            if event.key == pygame.K_1:
                fps = 5
            if event.key == pygame.K_1:
                fps = 10
