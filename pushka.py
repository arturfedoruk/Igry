import math
from random import choice
import pygame


FPS = 30
g = 1.5
score = 0
timer = 0

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

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=WIDTH/20, y=HEIGHT*3/4):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
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
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
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

        self.vy -= g

    def draw(self):
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
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x-obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            return True
        else:
            return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-HEIGHT*3/4) / (event.pos[0]-WIDTH/20))
        if self.f2_on:
            self.color = ORANGE
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.line(
            self.screen,
            BLACK,
            (WIDTH/20, HEIGHT*3/4),
            (WIDTH/20 + (self.f2_power + 10) * math.cos(self.an),
             HEIGHT*3/4 + (self.f2_power + 10) * math.sin(self.an)),
            16
        )
        pygame.draw.line(
            self.screen,
            self.color,
            (WIDTH/20, HEIGHT*3/4),
            (WIDTH/20 + (self.f2_power + 10) * math.cos(self.an),
             HEIGHT*3/4 + (self.f2_power + 10) * math.sin(self.an)),
            10
        )
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
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = ORANGE
        else:
            self.color = GREY


class Target:
    def __init__(self, screen: pygame.Surface,
                 x = choice(range(600, 780)),
                 y = choice(range(300, 550)),
                 r = choice(range(10, 30))
                 ):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = r
        self.color = RED
        self.live = 1

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = choice(range(600, 780))
        self.y = choice(range(300, 550))
        self.r = choice(range(10, 30))
        self.color = RED

    def draw(self):
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
        if t.live ==1:
            t.draw()

    for b in balls:
        if b.live <= 2 * FPS:
            b.draw()
        else:
            balls.remove(b)

    score_text = font.render("score = " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

    if timer > 0:
        timer -= 1
        bullet_text = font.render(
            "Вы поразили последнюю цель за " + str(bullet) + " выстрелов",
            True, BLACK
        )
        screen.blit(bullet_text, (WIDTH/8, HEIGHT/8))

    pygame.display.update()

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN and timer == 0:
            gun.fire2_start()
        elif event.type == pygame.MOUSEBUTTONUP and timer == 0:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.evolve()
        for t in targets:
            if b.hittest(t) and timer == 0:
                timer += 1.5*FPS
                t.live = 0
                score += 1
                balls.remove(b)

    gun.power_up()
    for t in targets:
        if t.live == 0:
            t.new_target()
    if timer == 1:
        for t in targets:
            t.live = 1
            bullet = 0

pygame.quit()
