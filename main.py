import os
import sys

import pygame

# инициализируем pygame
pygame.init()
# устанавливаем расширение 800 на 600
width, height = 800, 600
size = width, height
screen = pygame.display.set_mode(size)

# инициалищируем pygame.Clock() и ставим 60 FPS
FPS = 60
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
buttons_group = pygame.sprite.Group()

# вводим переменные громкости музыки и звуковых эффектов
music_level = 0.5
sound_effects_level = 0.5
# играем непрерывную музыку
pygame.mixer.music.load('data/sound_effects/music.wav')
pygame.mixer.music.set_volume(music_level)
pygame.mixer.music.play(loops=-1)


# функция загрузки изображения
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # загружаем полное имя файла
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Ошибка загрузки файла')
        raise SystemExit(message)
    # преобразуем фон изображения, если передан colorkey
    if colorkey:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# функция загрузки карты уровня
def load_level(filename="level.txt"):
    # передаем имя файла
    filename = "levels/" + filename
    # открываем файл
    try:
        with open(filename, 'r') as map_file:
            level = [line.strip() for line in map_file]
    except:
        print(f'No file with name "{filename}" in folder "levels"')
    # загружаем список карты
    finish_map = []
    for st in level:
        a = []
        for elem in st:
            a.append(elem)
        finish_map.append(a)
    return finish_map


load_level()

# передаем изображения всех кнопок в словарь
buttons = {'home_btn': load_image("home_button.png"), 'minus_btn': load_image("minus.png"),
           'plus_btn': load_image("plus.png"), 'mute_btn': load_image("mute.png"),
           'settings_btn': load_image("settings_button.png"), 'unmute_btn': load_image("unmute.png"),
           'play_btn': load_image("play_button.png"), 'return_btn': load_image("return_button.png")}

# создание списков для сменяющихся картинок между собой по очереди
rightwalking = [pygame.image.load('data/sprites/right_1.png'),
                pygame.image.load('data/sprites/right_2.png'),
                pygame.image.load('data/sprites/right_3.png'),
                pygame.image.load('data/sprites/right_4.png'),
                pygame.image.load('data/sprites/right_5.png'),
                pygame.image.load('data/sprites/right_6.png')]

leftwalking = [pygame.image.load('data/sprites/left_1.png'),
               pygame.image.load('data/sprites/left_2.png'),
               pygame.image.load('data/sprites/left_3.png'),
               pygame.image.load('data/sprites/left_4.png'),
               pygame.image.load('data/sprites/left_5.png'),
               pygame.image.load('data/sprites/left_6.png')]

fly = [pygame.image.load('data/sprites/fly_1.png')]

background = pygame.image.load('data/main_fon.png')
defoltplace = pygame.image.load('data/sprites/idle.png')

# загружаем карту
level_map = load_level()
# загружаем изображения самой игры
tile_images = {
    'thorn': load_image("thorns.png"),
    'block': load_image("block.png"),
}

# Местоположение персонажа относительно экрана
x_coord = 50
y_coord = 230
width_of_player = 61  # Размер спрайта в писелях ( ширина )
height_of_player = 70  # Размер спрайта в пикселях ( высота )
speed = 5

# Ставим изначальное значение прыжка и бега на False
jump = False
jump_height = 10

left = False
right = False

# Счётчик для смены анимаций
animation = 0


# функция выхода из игры
def terminate():
    pygame.quit()
    sys.exit()


# стартовый экран, из которого можно перейти в настройки и саму игру
def start_screen():
    # список строк текста
    intro_text = ['Pygame Project', 'Перед началом игры ознакомьтесь с файлом read_before_play.txt,',
                  'который лежит в папке с вашей программой.']

    # фон стартового экрана
    fon = pygame.transform.scale(load_image('start_fon.png'), (width, height))
    screen.blit(fon, (0, 0))

    # выводим все строки
    font_for_title = pygame.font.Font(None, 60)
    string_rendered = font_for_title.render(intro_text[0], 1, pygame.Color((127, 0, 255)))
    screen.blit(string_rendered, (242, 50))
    font_about = pygame.font.Font(None, 30)
    string_about1 = font_about.render(intro_text[1], 1, pygame.Color((127, 0, 255)))
    screen.blit(string_about1, (20, 150))
    string_about2 = font_about.render(intro_text[2], 1, pygame.Color((127, 0, 255)))
    screen.blit(string_about2, (20, 175))

    # выводим кнопки настроек и играть на экран
    screen.blit(buttons['settings_btn'], (750, 0))
    screen.blit(buttons['play_btn'], (130, 200))

    # цикл стартового экрана
    while True:
        for event in pygame.event.get():
            coord = pygame.mouse.get_pos()
            # screen.blit(cursor_img, coord)
            if event.type == pygame.QUIT:
                # выходим из игры, если пользователь закрыл программу
                terminate()
            if event.type == pygame.MOUSEMOTION:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                # проверяем, куда нажал пользователь
                if 750 <= event.pos[0] <= 800 and 0 <= event.pos[1] <= 50:
                    settings_screen()
                elif 130 <= event.pos[0] <= 630 and 200 <= event.pos[1] <= 575:
                    main_screen()
        # обновляем экран
        pygame.display.flip()
        clock.tick(FPS)


# экран настроек, в котором можно изменить громкость музыки и звуковых эффектов
def settings_screen(in_game=False):
    # глобализируем переменные
    global music_level, sound_effects_level

    # загружаем задний фон
    fon = pygame.transform.scale(load_image('settings_fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))

    # выводим все кнопки
    screen.blit(buttons['home_btn'], (748, 2))
    screen.blit(buttons['minus_btn'], (450, 150))
    screen.blit(buttons['plus_btn'], (270, 150))
    screen.blit(buttons['minus_btn'], (450, 350))
    screen.blit(buttons['plus_btn'], (270, 350))
    # если пользователь, вышел из игры в настройки,
    # то есть возможность вернуться назад с помозью одной кнопки "return"
    if in_game:
        screen.blit(buttons['return_btn'], (2, 2))

    # выводим строки текста
    text = ['Громкость музыки', 'Громкость звуковых эффектов']
    font_for_title = pygame.font.Font(None, 50)
    string_1 = font_for_title.render(text[0], 1, pygame.Color((127, 0, 255)))
    screen.blit(string_1, (242, 100))
    string_2 = font_for_title.render(text[1], 1, pygame.Color((127, 0, 255)))
    screen.blit(string_2, (130, 300))

    # цикл экрана настроек
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # выходим из игры, если пользователь закрыл программу
                terminate()
            if event.type == pygame.MOUSEMOTION:
                pass
                # cursor.rect.topleft = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                # проверяем, куда нажал пользователь
                if 748 <= event.pos[0] <= 800 and 0 <= event.pos[1] <= 50:
                    start_screen()
                if in_game:
                    if 0 <= event.pos[0] <= 50 and 0 <= event.pos[1] <= 50:
                        main_screen()
                # если это одна из кнопок изменения звука,
                # то изменяем переменные music_level или sound_effects_level соответственно нажатой кнопки
                if 450 <= event.pos[0] <= 514 and 150 <= event.pos[1] <= 214:
                    music_level -= 0.1
                    pygame.mixer.music.set_volume(music_level)
                if 270 <= event.pos[0] <= 334 and 150 <= event.pos[1] <= 214:
                    music_level += 0.1
                    pygame.mixer.music.set_volume(music_level)
                if 450 <= event.pos[0] <= 514 and 350 <= event.pos[1] <= 414:
                    sound_effects_level -= 0.1
                if 270 <= event.pos[0] <= 334 and 350 <= event.pos[1] <= 414:
                    sound_effects_level += 0.1
        # обновляем экран
        pygame.display.flip()
        clock.tick(FPS)


# класс других спрайтов
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, x, y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(x, y)


# класс спрайтов кнопок на главном экране
class Buttons(pygame.sprite.Sprite):
    # инициализируем
    def __init__(self):
        super().__init__(buttons_group)
        self.home_btn = buttons['home_btn']
        self.settings_btn = buttons['settings_btn']

    # выводим на экран
    def draw(self, screen):
        screen.blit(buttons['settings_btn'], (750, 0))
        screen.blit(buttons['home_btn'], (2, 2))


# класс игрока
class Player(pygame.sprite.Sprite):
    global x_coord, y_coord

    # инициализируем
    def __init__(self, x_coord, y_coord):
        super().__init__(player_group, all_sprites)
        self.image = defoltplace
        self.rect = self.image.get_rect().move(x_coord, y_coord)

    # функция отвечающая за передвижения персонажа
    def update(self, x_coord, y_coord):
        global animation
        # определяем скорость изменения анимаций (зависит от частоты смены кадров)
        if animation + 1 >= 60:
            animation = 0
        if left:
            # анимация при беге налево
            self.image = leftwalking[animation // 10]
            self.rect = self.image.get_rect().move(x_coord, y_coord)
            animation += 1
        elif right:
            # анимация при беге направо
            self.image = rightwalking[animation // 10]
            self.rect = self.image.get_rect().move(x_coord, y_coord)
            animation += 1
        elif jump:
            # анимация прыжка
            self.image = fly[animation // 10]
            self.rect = self.image.get_rect().move(x_coord, y_coord)
            animation += 1
        else:
            # иначе изначальное положение персонажа
            self.image = defoltplace
            self.rect = self.image.get_rect().move(x_coord, y_coord)


class Camera(object):
    def __init__(self):
        self.dx = 0

    def apply(self, obj, way):
        if way == 'left':
            obj.rect.x -= self.dx
        elif way == 'right':
            obj.rect.x += self.dx

    def update(self, target, way):
        if way == 'left':
            self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        elif way == 'right':
            self.dx = (target.rect.x + target.rect.w // 2 - width // 2)


# фцнкция генерации уровня с .txt файла
def generate_level():
    # инициализируем переменные
    global x_coord, y_coord
    # загружаем карту
    finish_map = load_level()
    for y in range(len(finish_map)):
        for x in range(len(finish_map[y])):
            if finish_map[y][x] == '@':
                x_coord = x * 50
                y_coord = y * 50
            elif finish_map[y][x] == '#':
                Tile('block', x * 50, y * 50 + 20)
            elif finish_map[y][x] == '%':
                Tile('thorn', x * 50, y * 50 + 20)


# главный экран
def main_screen():
    global jump, jump_height, x_coord, y_coord, left, right, animation

    # загружаем фон
    fon_image = pygame.transform.scale(load_image('main_fon.png'), (width, height))
    screen.blit(fon_image, (0, 0))

    # выводим кнопки настроек и возращения на стартовый экран
    buttons_class = Buttons()
    buttons_class.draw(screen)

    # выводим на экран игрока
    player = Player(x_coord, y_coord)

    # выводим спрайты
    generate_level()

    # создаем камеру
    # finish_map = load_level()
    # camera = Camera()

    # цикл главного экрана
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # выходим из игры, если пользователь закрыл программу
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # проверяем, куда нажал пользователь
                if 750 <= event.pos[0] <= 800 and 0 <= event.pos[1] <= 50:
                    settings_screen(True)
                elif 0 <= event.pos[0] <= 50 and 0 <= event.pos[1] <= 50:
                    start_screen()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and x_coord > 5:
            # бег при нажатии кнопки влево
            x_coord -= speed
            left = True
            right = False
        elif keys[pygame.K_RIGHT] and x_coord < 800 - width_of_player - 5:
            # бег при нажатии кнопки вправо
            x_coord += speed
            left = False
            right = True
        else:
            left = False
            right = False
            animation = 0
        if not jump:
            # если персонаж не в прыжке, возможность прыжка кнопкой вверх
            if keys[pygame.K_UP]:
                jump = True
        else:
            # скорость падения, высота прыжка и момент остановки прыжка
            if jump_height >= -10:
                if jump_height < 0:
                    y_coord += (jump_height ** 2) / 2
                else:
                    y_coord -= (jump_height ** 2) / 2
                jump_height -= 1
            else:
                jump = False
                jump_height = 10
        # обновляем экран
        screen.blit(fon_image, (0, 0))
        buttons_class.draw(screen)
        all_sprites.update(x_coord, y_coord)
        # изменяем ракурс камеры
        # camera.update(player)
        # обновляем положение всех спрайтов
        # for sprite in all_sprites:
        # if left:
        # camera.apply(sprite, 'left')
        # if right:
        # camera.apply(sprite, 'right')
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


# открываем игру с главного экрана
if __name__ == '__main__':
    main_screen()
