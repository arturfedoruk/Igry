# Игра "Шарики".

import pygame
from pygame.draw import *
from random import randint
from random import choice
pygame.init()

# Устанавливаемое заранее значение желаемого количества кадров в секунду.
FPS = 30
# Устанавливаемое заранее желательное значение разрешения окна игры.
screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
# Список цветов (можно изменять и добавлять свои).
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
clicks = 0
# Значение максимальной скорости шара (пикселей/кадр).
VMAX = 25
# Настройки наград: начальный счет, награда за попадание по большому и маленькому шарику.
score = 0
REWARD_FOR_BIG = 1
REWARD_FOR_SMALL = 5
REWARD_FOR_SQUARE = 10
# На экране всегна находится один маленький (более ценный) и большой (менее ценный) шарик.
# Далее в переменных индекс 1 относится к маленькому шарику, индекс 2 - к большому.


class SmallBall:
    def __init__(self):
        '''
        Создает маленький шарик.
        r - радиус
        x, y - координаты того, где создается
        color - его цвет
        '''
        self.screen = screen
        self.r = 50
        self.x = randint(self.r, screen_width - self.r)
        self.y = randint(self.r, screen_height - self.r)
        self.vx = randint(-VMAX, VMAX)
        self.vy = randint(-VMAX, VMAX)
        self.color = choice(COLORS)
        self.reward = REWARD_FOR_SMALL

    def draw(self):
        '''
        Отрисовывает шарик в точке
        '''
        circle(screen, self.color, (self.x, self.y), self.r)
        circle(screen, WHITE, (self.x, self.y), self.r, 2)

    def update(self):
        '''
        Обновляет шарик после попадания
        '''
        self.x = randint(self.r, screen_width - self.r)
        self.y = randint(self.r, screen_height - self.r)
        self.vx = randint(-VMAX, VMAX)
        self.vy = randint(-VMAX, VMAX)
        self.color = choice(COLORS)

    def reflection(self):
        '''
        Задает отражение от стенок экрана
        '''
        if self.x <= self.r and self.vx <= 0:
            # Левая стенка
            self.x = self.r
            self.vx = randint(0, VMAX)
            self.vy = randint(-VMAX, VMAX)
        elif self.x >= screen_width - self.r and self.vx >= 0:
            # Правая стенка
            self.x = screen_width - self.r
            self.vx = randint(-VMAX, 0)
            self.vy = randint(-VMAX, VMAX)
        elif self.y <= self.r and self.vy <= 0:
            # Верхняя стенка
            self.y = self.r
            self.vy = randint(0, VMAX)
            self.vx = randint(-VMAX, VMAX)
        elif self.y >= screen_height - self.r and self.vy >= 0:
            # Нижняя стенка
            self.y = screen_height - self.r
            self.vy = randint(-VMAX, 0)
            self.vx = randint(-VMAX, VMAX)

    def check_click(self, event):
        if (event.pos[0] - self.x)**2 + (event.pos[1] - self.y)**2 <= self.r**2:
            return True
        else:
            return False


class BigBall:
    def __init__(self):
        '''
        Создает большой шарик.
        r - радиус
        x, y - координаты того, где создается
        color - его цвет
        '''
        self.screen = screen
        self.r = 100
        self.x = randint(self.r, screen_width - self.r)
        self.y = randint(self.r, screen_height - self.r)
        self.vx = randint(-VMAX, VMAX)
        self.vy = randint(-VMAX, VMAX)
        self.color = choice(COLORS)
        self.reward = REWARD_FOR_BIG

    def draw(self):
        '''
        Отрисовывает шарик в точке
        '''
        circle(screen, self.color, (self.x, self.y), self.r)
        circle(screen, WHITE, (self.x, self.y), self.r, 2)

    def update(self):
        '''
        Обновляет шарик после попадания
        '''
        self.x = randint(self.r, screen_width - self.r)
        self.y = randint(self.r, screen_height - self.r)
        self.vx = randint(-VMAX, VMAX)
        self.vy = randint(-VMAX, VMAX)
        self.color = choice(COLORS)

    def reflection(self):
        '''
        Задает отражение от стенок экрана
        '''
        if self.x <= self.r and self.vx <= 0:
            # Левая стенка
            self.x = self.r
            self.vx = randint(0, VMAX)
            self.vy = randint(-VMAX, VMAX)
        elif self.x >= screen_width - self.r and self.vx >= 0:
            # Правая стенка
            self.x = screen_width - self.r
            self.vx = randint(-VMAX, 0)
            self.vy = randint(-VMAX, VMAX)
        elif self.y <= self.r and self.vy <= 0:
            # Верхняя стенка
            self.y = self.r
            self.vy = randint(0, VMAX)
            self.vx = randint(-VMAX, VMAX)
        elif self.y >= screen_height - self.r and self.vy >= 0:
            # Нижняя стенка
            self.y = screen_height - self.r
            self.vy = randint(-VMAX, 0)
            self.vx = randint(-VMAX, VMAX)

    def check_click(self, event):
        if (event.pos[0] - self.x)**2 + (event.pos[1] - self.y)**2 <= self.r**2:
            return True
        else:
            return False


class Square:
    def __init__(self):
        '''
        Создает квадратик.
        r - половина стороны квадрата
        x, y - координаты его центра
        color - его цвет
        '''
        self.screen = screen
        self.r = 20
        self.x = randint(self.r, screen_width - self.r)
        self.y = randint(self.r, screen_height - self.r)
        self.vx = randint(-VMAX, VMAX)
        self.vy = randint(-VMAX, VMAX)
        self.color = choice(COLORS)
        self.reward = REWARD_FOR_SQUARE

    def draw(self):
        '''
        Отрисовывает квадратик в точке
        '''
        rect(screen, self.color, (self.x - self.r, self.y - self.r, 2*self.r, 2*self.r))
        rect(screen, WHITE, (self.x - self.r, self.y - self.r, 2 * self.r, 2 * self.r), 2)

    def update(self):
        '''
        Обновляет квадратик после попадания
        '''
        self.x = randint(self.r, screen_width - self.r)
        self.y = randint(self.r, screen_height - self.r)
        self.vx = randint(-VMAX, VMAX)
        self.vy = randint(-VMAX, VMAX)
        self.color = choice(COLORS)

    def reflection(self):
        '''
        Задает отражение от стенок экрана
        '''
        if self.x <= self.r and self.vx <= 0:
            # Левая стенка
            self.x = self.r
            self.vx = randint(0, VMAX)
            self.vy = randint(-VMAX, VMAX)
        elif self.x >= screen_width - self.r and self.vx >= 0:
            # Правая стенка
            self.x = screen_width - self.r
            self.vx = randint(-VMAX, 0)
            self.vy = randint(-VMAX, VMAX)
        elif self.y <= self.r and self.vy <= 0:
            # Верхняя стенка
            self.y = self.r
            self.vy = randint(0, VMAX)
            self.vx = randint(-VMAX, VMAX)
        elif self.y >= screen_height - self.r and self.vy >= 0:
            # Нижняя стенка
            self.y = screen_height - self.r
            self.vy = randint(-VMAX, 0)
            self.vx = randint(-VMAX, VMAX)

    def check_click(self, event):
        if ((event.pos[0] <= (self.x + self.r)) and
                (event.pos[0] >= (self.x - self.r)) and
                (event.pos[1] <= (self.y + self.r)) and
                (event.pos[1] >= (self.y - self.r))):
            return True
        else:
            return False


pygame.display.update()
clock = pygame.time.Clock()
figures = []
finished = False

# Создаем изначальные шарики с изначальными скоростями
big_ball_1 = BigBall()
figures.append(big_ball_1)
small_ball_1 = SmallBall()
figures.append(small_ball_1)
square_1 = Square()
figures.append(square_1)


while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 or event.button == 3:
                clicks += 1
                for f in figures:
                    if f.check_click(event):
                        # Регистрируем попадание по  шарику, увеличиваем счет и пересоздаем его.
                        score += f.reward
                        print("Ваш счет на данный момент:", score)
                        f.update()

    for f in figures:
        # Изменение координат шариков между кадрами.
        f.x += f.vx
        f.y += f.vy
        # Проверка и реализация столкновения
        f.reflection()
        # Отрисовка шариков на новом кадре.
        f.draw()

    pygame.display.update()
    screen.fill(BLACK)

print("Итого ваш финальный счет составляет", score, "очков, было совершено", clicks, "нажатий мышкой. Вы молодец!")
pygame.quit()
