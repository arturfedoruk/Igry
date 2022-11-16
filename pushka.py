from random import choice
import pygame
from math import *


# Глобальные переменные системы: ФПС, ускорение свободного падения,
# счетчик очков и таймер, использующийся в некоторых механиках
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

# Переменные, использующиеся при при построении функций
gun_velocity = 10
gun_initial_power = 10
shard_velocity = 20
X0 = WIDTH/20
Y0 = HEIGHT*3/4


class Bullet:
    def __init__(self, screen, gun):
        """ Конструктор класса Bullet.

        x, y - начальное положение снаряда по горизонтали и вертикали
        r - радиус
        vx, vy - скорости снаряда по горизонтали и вертикали
        color - его цвет
        lifetimer - таймер, использующийся при проверке, нужно ли отрисовывать снаряд
        """
        global bullets
        self.screen = screen
        self.x = gun.x
        self.y = Y0
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.lifetimer = 1
        bullets.append(self)

    def evolve(self):
        """Описывает эволюцию положения и скоростей снаряда.

        Учитывается гравитация, столкновение со стенками
        """
        self.collided_with_edges()
        self.life_or_death()
        self.differential()

    def collided_with_edges(self):
        """Воздействие столкновения с краями экрана"""
        if (self.x >= WIDTH - self.r) and (self.vx > 0):
            self.x = WIDTH - self.r
            self.vx = -self.vx / 2
        elif (self.x <= self.r) and (self.vx < 0):
            self.x = self.r
            self.vx = -self.vx / 2
        elif self.y >= HEIGHT - 4*self.r:
            self.y = HEIGHT - 4*self.r
            self.vy = - self.vy / 2
            self.vx = self.vx / 2
            if abs(self.vy) <= 5:
                self.vy = 0

    def life_or_death(self):
        """описывает механизм исчезновения снаряда с экрана"""
        if self.vx == 0 or self.vy == 0:
            self.lifetimer += 1
        if self.lifetimer <= FPS:
            self.draw()
            # когда снаряд лежит на земле неподвижно более одной секунды, он исчезает...
        else:
            bullets.remove(self)
            # ... и удаляется из реестра снарядов

    def differential(self):
        """описывает изменение скорости и координаты снаряда"""
        self.x += self.vx
        self.y -= self.vy
        self.vy -= g

    def draw(self):
        """Отрисовывает снаряд"""
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

    def hit_test(self, obj):
        """
        Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        """
        if (self.x-obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            return True
        else:
            return False


class ExplosiveBullet(Bullet):
    def life_or_death(self):
        """То же, что и в классе Bullet"""
        self.lifetimer += 1
        if self.lifetimer <= FPS:
            self.draw()
        else:
            # через секунду разрывной патрон разрывается
            self.explosion()
            bullets.remove(self)
    
    def explosion(self):
        """Функция разрыва снаряда.
        После разрыва создается 8 осколка типа Shard, которые разлетаются симметрично
        """
        for j in range(8):
            angle = j*pi/4
            Shard(self.screen, self,
                  shard_velocity * cos(angle), shard_velocity * sin(angle))


class Shard(Bullet):
    def __init__(self, screen, ball, vx, vy):
        """ Конструктор класса Shard.

        x, y - начальное положение снаряда по горизонтали и вертикали
        r - радиус
        vx, vy - скорости снаряда по горизонтали и вертикали
        color - его цвет
        lifetimer - таймер, использующийся при проверке, нужно ли отрисовывать снаряд
        """
        global bullets
        self.screen = screen
        self.x = ball.x
        self.y = ball.y
        self.r = 3
        self.vx = vx
        self.vy = vy
        self.color = BLACK
        self.lifetimer = 1
        bullets.append(self)


class Gun:
    def __init__(self, screen):
        """Конструктор класса Gun.

        x - положение основания ствола пушки
        v - скорость пушки по горизонтали
        power - сила выстрела
        on - начало заряжания пушки
        angle - угол наклона пушки
        color - цвет
        bullet_type - тип выстреливаемого снаряда: стандартный или разрывной
        """
        self.x = X0
        self.v = 0
        self.screen = screen
        self.power = gun_initial_power
        self.on = 0
        self.angle = 1
        self.color = GREY
        self.bullet_type = "standard"

    def evolve(self):
        """Изменение состояния пушки"""
        self.power_up()
        self.motion()

    def fire_start(self):
        """Начало заряжания.

        Происходит при нажатии кнопки мыши
        """
        self.on = 1

    def measure_angle(self, event):
        """Вспомогательная функция, возвращающая угол, на который должна быть поднята пушка"""
        angle = atan2((event.pos[1] - Y0), (event.pos[0] - self.x))
        if pi/4 <= angle < pi/2:
            return pi/4
        elif pi/2 <= angle <= 3*pi/4:
            return 3*pi/4
        # пушка не может быть опущена ниже 45 градусов вниз
        else:
            return angle

    def switch_mode(self, event):
        """Функция изменения типа снарядов пушки"""
        if event.key == pygame.K_1:
            self.bullet_type = "standard"
        elif event.key == pygame.K_2:
            self.bullet_type = "explosive"

    def fire_end(self, event):
        """Выстрел снарядом. Происходит при отпускании левой кнопки мыши."""
        if self.bullet_type == "standard":
            self.fire_standard(event)
        elif self.bullet_type == "explosive":
            self.fire_explosive(event)

    def fire_standard(self, event):
        """Выстрел обычным снарядом.
        Начальные значения компонент скорости снаряда vx и vy зависят от положения мыши.
        """
        global shots
        shots += 1
        new_bullet = Bullet(self.screen, self)
        self.angle = self.measure_angle(event)
        new_bullet.vx = self.power * cos(self.angle)
        new_bullet.vy = - self.power * sin(self.angle)
        self.on = 0
        self.power = gun_initial_power

    def fire_explosive(self, event):
        """Выстрел разрывным снарядом.
        Начальные значения компонент скорости снаряда vx и vy зависят от положения мыши.
        """
        global shots
        shots += 1
        new_bullet = ExplosiveBullet(self.screen, self)
        self.angle = self.measure_angle(event)
        new_bullet.vx = self.power * cos(self.angle)
        new_bullet.vy = - self.power * sin(self.angle)
        self.on = 0
        self.power = gun_initial_power

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.angle = self.measure_angle(event)
        if self.on:
            self.color = ORANGE
        else:
            self.color = GREY

    def draw(self):
        """Отрисовывает пушку."""
        self.draw_body(self.x, Y0)
        self.draw_tracks(self.x, Y0)
        self.draw_barrel(self.x, Y0)

    def draw_barrel(self, x, y):
        """отрисовывает ствол"""
        pygame.draw.circle(
            self.screen,
            GREY,
            (x, y),
            10
        )
        pygame.draw.circle(
            self.screen,
            BLACK,
            (x, y),
            10,
            2
        )
        pygame.draw.line(
            self.screen,
            BLACK,
            (x, y),
            (x + (self.power + 10) * cos(self.angle),
             y + (self.power + 10) * sin(self.angle)),
            12
        )
        pygame.draw.line(
            self.screen,
            self.color,
            (x, y),
            (x + (self.power + 10) * cos(self.angle),
             y + (self.power + 10) * sin(self.angle)),
            6
        )

    def draw_body(self, x, y):
        """отрисовывает корпус"""
        pygame.draw.rect(
            screen,
            GREY,
            (x - X0, y + 3, 2*X0, 20),
            0, 0, 5, 5
        )
        pygame.draw.rect(
            screen,
            BLACK,
            (x - X0, y + 3, 2*X0, 20),
            2, 0, 5, 5
        )

    def draw_tracks(self, x, y):
        """отрисовывает гусеницы"""
        for i in range(0, int(2*X0), int(2*X0/5)):
            pygame.draw.circle(
                self.screen,
                GREY,
                (x - X0 + 10 + i, y + 23),
                10
            )
            pygame.draw.circle(
                self.screen,
                BLACK,
                (x - X0 + 10 + i, y + 23),
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

    def motion(self):
        if (self.x >= WIDTH - X0 and self.v > 0) or (self.x <= X0 and self.v < 0):
            self.v = 0
        self.x += self.v


class Target:
    def __init__(self, screen: pygame.Surface,
                 x=choice(range(30, WIDTH - 30)),
                 y=choice(range(50, int(Y0 - 50))),
                 r=choice(range(10, 30))
                 ):
        """Генератор класса Target

        x, y - положение цели по горизонтали и вертикали
        r - радиус мишени
        color - цвет
        live - статус, поражена ли цель или нет
        """
        global targets
        self.screen = screen
        self.x = x
        self.y = y
        self.r = r
        self.color = RED
        self.live = 1
        targets.append(self)

    def evolve(self):
        """Обновление состояния мишени"""
        self.motion()
        if self.live == 1:
            self.draw()
        elif self.live == 0:
            self.update()

    def update(self):
        """ Пересоздает цель после попадания по ней снарядом"""
        self.x = choice(range(30, WIDTH - 30))
        self.y = choice(range(50, int(Y0 - 50)))
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

    def motion(self):
        pass


class MovingTarget(Target):
    def __init__(self, screen: pygame.Surface,
                 x0=choice(range(30, WIDTH - 100)),
                 y0=choice(range(50, int(Y0 - 50))),
                 r=choice(range(10, 30))
                 ):
        """Генератор класса MovingTarget. Такие мишени двигаются по круговой траектории

        R - радиус траектории
        omega - угловая скорость движения цели по траектории
        x0, y0 - положение центра траектории
        x, y - положение цели по горизонтали и вертикали
        r - радиус мишени
        color - цвет
        live - статус, поражена ли цель или нет
        """
        global targets
        self.screen = screen
        self.R = choice(range(30, 100))
        self.omega = 0.1
        self.angle = 0
        self.x0 = x0
        self.y0 = y0
        self.x = self.x0 + self.R * cos(self.angle)
        self.y = self.y0 + self.R * sin(self.angle)
        self.r = r
        self.color = RED
        self.live = 1
        targets.append(self)

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

    def motion(self):
        """Функция движения цели по своей траектории"""
        self.angle += self.omega
        self.x = self.x0 + self.R * cos(self.angle)
        self.y = self.y0 + self.R * sin(self.angle)

    def update(self):
        """ Пересоздает цель после попадания по ней снарядом"""
        self.x0 = choice(range(100, WIDTH - 100))
        self.y0 = choice(range(100, int(Y0 - 50)))
        self.r = choice(range(10, 30))
        self.color = RED



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
shots = 0
bullets = []
targets = []
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()
# создание пушки и целей
gun = Gun(screen)
Target(screen, 200, 200)
Target(screen, 600, 200)
MovingTarget(screen, 400, 400)

finished = False
while not finished:
    screen.fill(WHITE)
    gun.draw()

    for t in targets:
        # обновление состояния мишеней
        t.evolve()

    # Табло счета
    score_text = font.render("score = " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

    if timer > 0:
        timer -= 1
        shots_text = font.render(
            "Вы поразили последнюю цель за " + str(shots) + " выстрелов",
            True, BLACK
        )
        screen.blit(shots_text, (WIDTH/8, HEIGHT*7/8))
        # надпись со статистикой попадания по последней цели,
        # появляется на некоторое время (при попадании по цели запускается таймер)

    for b in bullets:
        # движение снаряда
        b.evolve()
        for t in targets:
            # проверка попадания
            if b.hit_test(t) and t.live == 1:
                # запуск таймера (если он уже не запущен)
                if timer == 0:
                    timer += 1.5*FPS
                # цель поражена
                t.live = 0
                score += 1
                # снаряд после попадания исчезает
                bullets.remove(b)

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
            if event.button == 1 or event.button == 3:
                gun.fire_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
        elif event.type == pygame.KEYDOWN:
            gun.switch_mode(event)
            if event.key == pygame.K_d:
                gun.v = gun_velocity
            elif event.key == pygame.K_a:
                gun.v = -gun_velocity
        elif event.type == pygame.KEYUP:
            gun.v = 0

    gun.evolve()

    if timer == 1:
        for t in targets:
            t.live = 1
            shots = 0

# финальное табло, показывающее, сколько очков ты набрал
screen.fill(WHITE)
final_text = font.render("Ваш финальный счет составляет " + str(score) + " очков", True, BLACK)
screen.blit(final_text, (WIDTH/4, HEIGHT/2))
pygame.display.update()
pygame.time.wait(2000)

pygame.quit()
