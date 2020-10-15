import pygame
import sys
import time

pygame.init()

width = 640
height = 480
colourBlue = (0, 0, 64)

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("C:/Users/Ale/Proyectos/pygame/ladrillos/resources/bolita.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = int(width / 2)
        self.rect.centery = int(height / 2)
        self.speed = [3, 3]

    def update(self):
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
        if self.rect.right >= width or self.rect.left <= 0:
            self.speed[0] = -self.speed[0]

        self.rect.move_ip(self.speed)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("C:/Users/Ale/Proyectos/pygame/ladrillos/resources/paleta.png")
        self.rect = self.image.get_rect()
        self.rect.midbottom = (int(width / 2), int(height - 20))
        self.speed = [0, 0]

    def update(self, event):
        if event.key == pygame.K_LEFT and self.rect.left > 0:
            self.speed = [-10, 0]
        elif event.key == pygame.K_RIGHT and self.rect.right < width:
            self.speed = [10, 0]
        else:
            self.speed = [0, 0]
        self.rect.move_ip(self.speed)

class Brick(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("C:/Users/Ale/Proyectos/pygame/ladrillos/resources/ladrillo.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = position

class Wall(pygame.sprite.Group):
    def __init__(self, brickQty):
        pygame.sprite.Group.__init__(self)

        brick1 = Brick((0, 0))
        brick2 = Brick((100,100))

        posX = 0
        posY = 20

        for i in range(brickQty):
            brick = Brick((posX, posY))
            self.add(brick)
            posX += brick.rect.width
            if posX >= width:
                posX = 0
                posY += brick.rect.height

def JuegoTerminado():
    font = pygame.font.SysFont('Arial', 72)
    text = font.render('Game Over', True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = [int(width / 2), int(height / 2)]
    screen.blit(text, text_rect)
    pygame.display.flip()
    time.sleep(3)
    sys.exit()

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("brick")
clock = pygame.time.Clock()
pygame.key.set_repeat(30)
ball = Ball()
player = Player()
wall = Wall(50)

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            player.update(event)

    ball.update()

    if pygame.sprite.collide_rect(ball, player):
        ball.speed[1] = -ball.speed[1]

    list = pygame.sprite.spritecollide(ball, wall, False)
    if list:
        brick = list[0]
        cx = ball.rect.centerx
        if cx < brick.rect.left or cx > brick.rect.right:
            ball.speed[0] = -ball.speed[0]
        else:
            ball.speed[1] = -ball.speed[1]
        wall.remove(brick)

    if ball.rect.top >= height:
        JuegoTerminado()
    screen.fill(colourBlue)
    wall.draw(screen)

    screen.blit(ball.image, ball.rect)
    screen.blit(player.image, player.rect)
    pygame.display.flip()
