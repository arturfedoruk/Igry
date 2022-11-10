import math
from random import choice
import pygame


FPS = 30
g = 1.5
score = 0
timer = 0

# Цвета игры
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 160, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
GAME_COLORS = [RED, BLUE, YELLOW, ORANGE, GREEN, MAGENTA, CYAN]

# Параметры окна игры
WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=WIDTH/20, y=HEIGHT*3/4):
        """ Конструктор класса ball.

        x, y - начальное положение мяча по горизонтали и вертикали
        r - радиус
        vx, vy - скорости мяча по горизонтали и вертикали
        color - его цвет
        live - статус, нужно ли отрисовывать его
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 1

    def evolve(self):
        """Описывает эволюцию положения и скоростей мяча.

        Учитывается гравитация, столкновение со стенками
        """

        if self.x >= WIDTH - self.r:
            self.x = WIDTH - self.r
            self.vx = -self.vx / 2
        elif self.y >= HEIGHT - 4*self.r:
            self.y = HEIGHT - 4*self.r
            self.vy = - self.vy / 2
            self.vx = self.vx / 2
            if abs(self.vy) <= 5:
                self.vy = 0

        self.x += self.vx
        self.y -= self.vy

        if self.vx == 0 or self.vy == 0:
            self.live += 1
            # когда мячик лежит на земле неподвижно более двух секунд, он исчезает

        self.vy -= g

    def draw(self):
        """Отрисовывает мяч"""
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            self.r,
            2
        )

    def hittest(self, obj):
        """
        Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        """
        if (self.x-obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            return True
        else:
            return False


class Gun:
    def __init__(self, screen):
        """Конструктор класса Gun.

        power - сила выстрела
        on - начало заряжания пушки
        angle - угол наклона пушки
        color - цвет
        """
        self.screen = screen
        self.power = 10
        self.on = 0
        self.angle = 1
        self.color = GREY

    def fire_start(self):
        """Начало заряжания.

        Происходит при нажатии кнопки мыши
        """
        self.on = 1

    def fire_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        self.angle = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.power * math.cos(self.angle)
        new_ball.vy = - self.power * math.sin(self.angle)
        balls.append(new_ball)
        self.on = 0
        self.power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.angle = math.atan((event.pos[1]-HEIGHT*3/4) / (event.pos[0]-WIDTH/20))
        if self.on:
            self.color = ORANGE
        else:
            self.color = GREY

    def draw(self):
        """Отрисовывает пушку."""
        # ствол
        pygame.draw.line(
            self.screen,
            BLACK,
            (WIDTH/20, HEIGHT*3/4),
            (WIDTH/20 + (self.power + 10) * math.cos(self.angle),
             HEIGHT*3/4 + (self.power + 10) * math.sin(self.angle)),
            16
        )
        pygame.draw.line(
            self.screen,
            self.color,
            (WIDTH/20, HEIGHT*3/4),
            (WIDTH/20 + (self.power + 10) * math.cos(self.angle),
             HEIGHT*3/4 + (self.power + 10) * math.sin(self.angle)),
            10
        )
        # корпус
        pygame.draw.rect(
            screen,
            GREY,
            (-10, HEIGHT*3/4 - 5, WIDTH/20 + 15, 20),
            0, 0, 0, 5
        )
        pygame.draw.rect(
            screen,
            BLACK,
            (-10, HEIGHT*3/4 - 5, WIDTH/20 + 15, 20),
            2, 0, 0, 5
        )
        # гусеницы
        for i in range(0, WIDTH//20 + 10, WIDTH//50):
            pygame.draw.circle(
                self.screen,
                GREY,
                (WIDTH/20 - i, HEIGHT*3/4 + 15),
                10
            )
            pygame.draw.circle(
                self.screen,
                BLACK,
                (WIDTH/20 - i, HEIGHT*3/4 + 15),
                10,
                2
            )

    def power_up(self):
        if self.on:
            if self.power < 100:
                self.power += 1
            self.color = ORANGE
        else:
            self.color = GREY


class Target:
    def __init__(self, screen: pygame.Surface,
                 x=choice(range(600, 780)),
                 y=choice(range(300, 550)),
                 r=choice(range(10, 30))
                 ):
        """Генератор класса Target

        x, y - положение цели по горизонтали и вертикали
        r - радиус мишени
        color - цвет
        live - статус, поражена ли цель или нет
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = r
        self.color = RED
        self.live = 1

    def update(self):
        """ Пересоздает цель после попадания по ней мячом"""
        self.x = choice(range(600, 780))
        self.y = choice(range(300, 550))
        self.r = choice(range(10, 30))
        self.color = RED

    def draw(self):
        """ Отрисовывает цель"""
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            self.r,
            2
        )


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
targets = []
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Target(screen, 700, 300)
targets.append(target1)
target2 = Target(screen, 700, 500)
targets.append(target2)

finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()

    for t in targets:
        if t.live == 1:
            t.draw()

    for b in balls:
        if b.live <= 2 * FPS:
            b.draw()
            # когда мячик лежит на земле неподвижно более двух секунд, он исчезает...
        else:
            balls.remove(b)
            # ... и удаляется из реестра мячей

    # Табло счета
    score_text = font.render("score = " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

    if timer > 0:
        timer -= 1
        bullet_text = font.render(
            "Вы поразили последнюю цель за " + str(bullet) + " выстрелов",
            True, BLACK
        )
        screen.blit(bullet_text, (WIDTH/8, HEIGHT/8))
        # надпись со статистикой попадания по последней цели,
        # появляется на некоторое время (при попадании по цели запускается таймер)

    pygame.display.update()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        # пока горит надпись со статистикой попадания по последней
        # цели (т.е. пока идет таймер) стрелять нельзя
        elif event.type == pygame.MOUSEBUTTONDOWN and timer == 0:
            gun.fire_start()
        elif event.type == pygame.MOUSEBUTTONUP and timer == 0:
            gun.fire_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        # движение мячика
        b.evolve()
        for t in targets:
            # проверка попадания
            if b.hittest(t) and timer == 0:
                # запуск таймера
                timer += 1.5*FPS
                # цель поражена
                t.live = 0
                score += 1
                # мячик после попадания исчезает
                balls.remove(b)

    gun.power_up()
    for t in targets:
        if t.live == 0:
            t.update()
    if timer == 1:
        for t in targets:
            t.live = 1
            bullet = 0

pygame.quit()
