import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption('Sprite animation')

# Создание списков для сменяющихся картинок между собой по очереди
rightwalking = [pygame.image.load('sprites/right_1.png'),
                pygame.image.load('sprites/right_2.png'), pygame.image.load('sprites/right_3.png'),
                pygame.image.load('sprites/right_4.png'), pygame.image.load('sprites/right_5.png'),
                pygame.image.load('sprites/right_6.png')]

leftwalking = [pygame.image.load('sprites/left_1.png'),
               pygame.image.load('sprites/left_2.png'), pygame.image.load('sprites/left_3.png'),
               pygame.image.load('sprites/left_4.png'), pygame.image.load('sprites/left_5.png'),
               pygame.image.load('sprites/left_6.png')]

fly = [pygame.image.load('sprites/fly_1.png')]

background = pygame.image.load('data/start_fon.png')
defoltplace = pygame.image.load('sprites/idle.png')

clock = pygame.time.Clock()

# Местоположение персонажа относительно экрана
x_coord = 50
y_coord = 525
width = 61  # Размер спрайта в писелях ( ширина )
height = 70  # Размер спрайта в пикселях ( высота )
speed = 5

# Ставим изначальное значение прыжка и бега на False
Jump = False
JumpHight = 10

left = False
right = False

# Счётчик для смены анимаций
animation = 0


# Функция отвечающая за передвижения персонажа
def Main():
    global animation
    screen.blit(background, (0, 0))  # Ставим задний фон

    if animation + 1 >= 60:  # Определяем скорость изменения анимаций ( зависит от частоты смены кадров )
        animation = 0

    if left:
        screen.blit(leftwalking[animation // 10], (x_coord, y_coord))  # Анимация при беге налево
        animation += 1
    elif right:
        screen.blit(rightwalking[animation // 10], (x_coord, y_coord))  # Анимация при беге направо
        animation += 1
    elif Jump:
        screen.blit(fly[animation // 10], (x_coord, y_coord))  # Анимация прыжка
        animation += 1
    else:
        screen.blit(defoltplace, (x_coord, y_coord))  # Иначе изначальное положение персонажа

    pygame.display.update()


run = True
while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x_coord > 5:  # Бег при нажатии кнопки влево
        x_coord -= speed
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and x_coord < 800 - width - 5:  # Бег при нажатии кнопки вправо
        x_coord += speed
        left = False
        right = True
    else:
        left = False
        right = False
        animation = 0
    if not Jump:
        if keys[pygame.K_UP]:  # Если персонаж не в прыжке, возможность прыжка кнопкой вверх
            Jump = True

    else:
        # Cкорость падения, высота прыжка и момент остановки прыжка
        if JumpHight >= -10:
            if JumpHight < 0:
                y_coord += (JumpHight ** 2) / 2
            else:
                y_coord -= (JumpHight ** 2) / 2
            JumpHight -= 1
        else:
            Jump = False
            JumpHight = 10

    Main()
