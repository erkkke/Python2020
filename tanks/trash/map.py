import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
GameOver_single = pygame.image.load('pic/game_over_single.jpg')
class Button:
    def __init__(self, text, x, y, width, height, function, active_colour, nonactive_colour, font):
        self.isActive = False
        self.active_colour = active_colour
        self.nonactive_colour = nonactive_colour
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.function = function
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

def game_over_scene(whoiam, score):
    font1 = pygame.font.SysFont('comicsansms', 30)
    font2 = pygame.font.SysFont('comicsansms', 30)
    Restart = Button('Restart', 175, 450, 150, 40, None, (0, 176, 0), (0, 70, 0), None)
    Quit = Button('Quit', 500, 450, 150, 40, None, (176, 0, 0), (70, 0, 0), None)
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

            mouse = pygame.mouse.get_pos()

            for button in buttons:
                if button.x <= mouse[0] <= button.x + button.width and button.y <= mouse[1] <= button.y + button.height:
                    button.isActive = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        action = button.text
                        show = False
                else: button.isActive = False

        if whoiam == 'winner':
            color = (0, 170, 0)
            text = 'You won!'
        else:
            color = (170, 0, 0)
            text = 'You lost, lucky next time!'

        message1 = font1.render(text, 1, color)
        message1Rect = message1.get_rect()
        message1Rect.center = (400, 340)

        message2 = font2.render(f'Your score: {score}', 1, color)
        message2Rect = message2.get_rect()
        message2Rect.center = (400, 390)

        screen.blit(GameOver_single, (0, 0))
        screen.blit(message1, message1Rect)
        screen.blit(message2, message2Rect)

        for button in buttons:
            button.draw()

        pygame.display.update()

whoiam = 'winner'
score = 3

game_over_scene(whoiam, score)