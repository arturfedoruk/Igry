# Игра "Шарики".

import pygame
from pygame.draw import *
from random import randint
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
num_of_colors = len(COLORS)
# Значение максимальной скорости шара (пикселей/кадр).
VMAX = 25
# Настройки наград: начальный счет, награда за попадание по большому и маленькому шарику.
score = 0
REWARD_FOR_BIG = 1
REWARD_FOR_SMALL = 5
# На экране всегна находится один маленький (более ценный) и большой (менее ценный) шарик.
# Далее в переменных индекс 1 относится к маленькому шарику, индекс 2 - к большому.


def new_small_ball():
    '''
    Создает новый маленький шарик.
    r1 - радиус
    x1, y1 - координаты того, где создается
    color1 - его цвет
    '''
    global x1, y1, r1, color1
    r1 = 50
    x1 = randint(r1, screen_width - r1)
    y1 = randint(r1, screen_height - r1)
    color1 = COLORS[randint(0, num_of_colors - 1)]
    circle(screen, color1, (x1, y1), r1)
    circle(screen, WHITE, (x1, y1), r1, 2)

def new_big_ball():
    '''
    Создает новый большой шарик.
    r2 - радиус
    x2, y2 - координаты того, где создается
    color2 - его цвет
    '''
    global x2, y2, r2, color2
    r2 = 100
    x2 = randint(r2, screen_width - r2)
    y2 = randint(r2, screen_height - r2)
    color2 = COLORS[randint(0, num_of_colors - 1)]
    circle(screen, color2, (x2, y2), r2)
    circle(screen, WHITE, (x2, y2), r2, 2)


def small_ball(x1, y1):
    '''
    Используется при воспроизведении маленького шара при смене кадра.
    x1, y1 - координаты
    '''
    circle(screen, color1, (x1, y1), r1)
    circle(screen, WHITE, (x1, y1), r1, 2)


def big_ball(x2, y2):
    '''
    Используется при воспроизведении ,большого шара при смене кадра.
    x1, y1 - координаты
    '''
    circle(screen, color2, (x2, y2), r2)
    circle(screen, WHITE, (x2, y2), r2, 2)


def rand_velocity():
    '''Возвращает скорость, по модулю меньшую, чем VMAX.'''
    return randint(-VMAX, VMAX)


def rand_reflected(v):
    '''
    Используется при отражении шара от стенки.
    Направление скорости изменяется, модуль скорости - случайный.
    '''
    if v > 0:
        return randint(-VMAX, 0)
    elif v < 0:
        return randint(0, VMAX)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

# Создаем изначальные шарики с изначальными скоростями
new_big_ball()
new_small_ball()
vx1 = rand_velocity()
vy1 = rand_velocity()
vx2 = rand_velocity()
vy2 = rand_velocity()

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 or event.button == 3:
                if ((event.pos[0] <= (x1 + r1)) and (event.pos[0] >= (x1 - r1)) and
                                                    (event.pos[1] <= (y1 + r1)) and
                                                    (event.pos[1] >= (y1 - r1))):
                    # Регистрируем попадание по маленькому шарику, увеличиваем счет и пересоздаем его.
                    score += REWARD_FOR_SMALL
                    print("Ваш счет на данный момент:", score)
                    new_small_ball()
                    vx1 = rand_velocity()
                    vy1 = rand_velocity()
                elif ((event.pos[0] <= (x2 + r2)) and (event.pos[0] >= (x2 - r2)) and
                                                    (event.pos[1] <= (y2 + r2)) and
                                                    (event.pos[1] >= (y2 - r2))):
                    # Регистрируем попадание по большому шарику, увеличиваем счет и пересоздаем его.
                    score += REWARD_FOR_BIG
                    print("Ваш счет на данный момент:", score)
                    new_big_ball()
                    vx2 = rand_velocity()
                    vy2 = rand_velocity()
    # Регистрируется прикосновение шарика со стеной и срабатывает его рандомное отражение.
    if (x1 >= (screen_width - r1) and vx1 > 0) or (x1 <= r1 and vx1 < 0):
        vx1 = rand_reflected(vx1)
        vy1 = rand_velocity()
    if (y1 >= (screen_height - r1) and vy1 > 0) or (y1 <= r1 and vy1 < 0):
        vy1 = rand_reflected(vy1)
        vx1 = rand_velocity()
    if (x2 >= (screen_width - r2) and vx2 > 0) or (x2 <= r2 and vx2 < 0):
        vx2 = rand_reflected(vx2)
        vy2 = rand_velocity()
    if (y2 >= (screen_height - r2) and vy2 > 0) or (y2 <= r2 and vy2 < 0):
        vy2 = rand_reflected(vy2)
        vx2 = rand_velocity()

    # Изменение координат шариков между кадрами.
    x1 += vx1
    x2 += vx2
    y1 += vy1
    y2 += vy2

    # Отрисовка шариков на новом кадре.
    small_ball(x1, y1)
    big_ball(x2, y2)

    pygame.display.update()
    screen.fill(BLACK)

print("Итого ваш финальный счет составляет", score, "очков. Вы молодец!")
pygame.quit()
