import pygame
import sys
import time


width = 640
height = 480
colourBlue = (0, 0, 64)
colourWhite = (255, 255, 255)

class Scene:

    def __init__(self):
        self.nextScene = False
        self.playing = True

    def read_events(self, events):
        pass

    def update(self):
        pass

    def draw_scene(self, screen):
        pass

    def change_scene(self, scene):
        self.nextScene = scene


class Controller:
    def __init__(self, title="", res=(width, height)):
        pygame.init()

        self.screen = pygame.display.set_mode(res)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.scene = None
        self.scenes = {}

    def run(self, initial_scene, fps=60):
        self.scene = self.scenes[initial_scene]
        playing = True
        while playing:
            self.clock.tick(fps)
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    playing = False
            self.scene.read_events(events)
            self.scene.update()
            self.scene.draw_scene(self.screen)
            self.choose_scene(self.scene.nextScene)
            if playing:
                playing = self.scene.playing
            pygame.display.flip()

        time.sleep(3)

    def choose_scene(self, next_scene):
        if next_scene:
            if next_scene not in self.scenes:
                self.add_scene(next_scene)
            self.scene = self.scenes[next_scene]

    def add_scene(self, scene_name):
        scene_class = scene_name + 'Scene'
        scene_obj = globals()[scene_class]
        self.scenes[scene_name] = scene_obj()


class Lvl1Scene(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.ball = Ball()
        self.player = Player()
        self.wall = Wall(50)
        self.puntuation = 0
        self.lifes = 3
        self.waitingServe = True
        pygame.key.set_repeat(30)

    def read_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.player.update(event)
                if self.waitingServe and event.key == pygame.K_SPACE:
                    self.waitingServe = False
                    if self.ball.rect.centerx < width / 2:
                        self.ball.speed = [3, -3]
                    else:
                        self.ball.speed = [-3, -3]

    def update(self):
        if self.waitingServe:
            self.ball.rect.midbottom = self.player.rect.midtop
        else:
            self.ball.update()

        if pygame.sprite.collide_rect(self.ball, self.player):
            self.ball.speed[1] = -self.ball.speed[1]

        list = pygame.sprite.spritecollide(self.ball, self.wall, False)
        if list:
            brick = list[0]
            cx = self.ball.rect.centerx
            if cx < brick.rect.left or cx > brick.rect.right:
                self.ball.speed[0] = -self.ball.speed[0]
            else:
                self.ball.speed[1] = -self.ball.speed[1]
            self.wall.remove(brick)
            self.puntuation += 10

        if self.ball.rect.top >= height:
            self.lifes -= 1
            self.waitingServe = True
        if self.lifes <= 0:
            self.change_scene('GameOver')

    def draw_scene(self, screen):
        screen.fill(colourBlue)
        self.show_puntuation(screen)
        self.show_lifes(screen)
        self.wall.draw(screen)

        screen.blit(self.ball.image, self.ball.rect)
        screen.blit(self.player.image, self.player.rect)

    def show_puntuation(self, screen):
        font = pygame.font.SysFont('Consolas', 20)
        text = font.render(str(self.puntuation).zfill(5), True, colourWhite)
        text_rect = text.get_rect()
        text_rect.topleft = [0, 0]
        screen.blit(text, text_rect)

    def show_lifes(self, screen):
        font = pygame.font.SysFont('Consolas', 20)
        string = "Lifes: " + str(self.lifes).zfill(2)
        text = font.render(string, True, colourWhite)
        text_rect = text.get_rect()
        text_rect.topright = [width, 0]
        screen.blit(text, text_rect)

class GameOverScene(Scene):
    def update(self):
        self.playing = False

    def draw_scene(self, screen):
        font = pygame.font.SysFont('Arial', 72)
        text = font.render('Game Over', True, colourWhite)
        text_rect = text.get_rect()
        text_rect.center = [int(width / 2), int(height / 2)]
        screen.blit(text, text_rect)
        pygame.display.flip()

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
        brick2 = Brick((100, 100))

        posX = 0
        posY = 20

        for i in range(brickQty):
            brick = Brick((posX, posY))
            self.add(brick)
            posX += brick.rect.width
            if posX >= width:
                posX = 0
                posY += brick.rect.height


controller = Controller('Arkanoid', (640, 480))
controller.add_scene('Lvl1')
controller.run('Lvl1')









