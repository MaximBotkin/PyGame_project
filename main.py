import os
import sys
import pygame
import PyQt5
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5 import uic
import sqlite3
import hashlib

# инициализируем pygame
pygame.init()
# устанавливаем расширение 800 на 600
width, height = 800, 600
size = width, height
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Bit Adventure')

# инициализируем pygame.Clock() и ставим 60 FPS
FPS = 60
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
thorns_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
buttons_group = pygame.sprite.Group()
finish_group = pygame.sprite.Group()

# вводим переменные громкости музыки и звуковых эффектов
music_level = 0.1
sound_effects_level = 0.5

# играем непрерывную музыку
pygame.mixer.music.load('data/sound_effects/music.wav')
pygame.mixer.music.set_volume(0)
pygame.mixer.music.play(loops=-1)

# звук падения
drop = pygame.mixer.Sound("data/sound_effects/drop.wav")
# звук нажатия кнопки
menu_up = pygame.mixer.Sound("data/sound_effects/menu-up.wav")
# звук победы
win_sound = pygame.mixer.Sound("data/sound_effects/win_music.wav")
# звук поражения
lose_sound = pygame.mixer.Sound("data/sound_effects/lose_music.wav")


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
def load_level(filename="level1.txt"):
    # передаем имя файла
    filename = "levels/" + filename
    # открываем файл
    try:
        with open(filename, 'r') as map_file:
            level = [line.strip() for line in map_file]
    except:
        print(f'No file with name "{filename}" in folder "levels"')
        sys.exit()
    # загружаем список карты
    finish_map = []
    for st in level:
        a = []
        for elem in st:
            a.append(elem)
        finish_map.append(a)
    return finish_map


# передаем изображения всех кнопок в словарь
buttons = {'home_btn': load_image("home_button.png"), 'minus_btn': load_image("minus.png"),
           'plus_btn': load_image("plus.png"), 'mute_btn': load_image("mute.png"),
           'settings_btn': load_image("settings_button.png"), 'unmute_btn': load_image("unmute.png"),
           'play_btn': load_image("play_button.png"), 'return_btn': load_image("return_button.png"),
           'next_btn': load_image("next.png"), 'previous_btn': load_image("return_button.png")}

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

# загружаем изображения самой игры
tile_images = {
    'thorn': load_image("thorns.png"),
    'block': load_image("block.png"),
    'clearblock': load_image("clear_block.png"),
    'waterblock': load_image("water_block.png"),
    'finish_flag': load_image("finish.png"),
}

# Местоположение персонажа относительно экрана
x_coord = 50
y_coord = 100
width_of_player = 61  # Размер спрайта в пикселях ( ширина )
height_of_player = 70  # Размер спрайта в пикселях ( высота )
speed = 5

# Ставим изначальное значение прыжка и бега на False
jump = False
jump_height = 10
is_flying = True

left = False
right = False

# Счётчик для смены анимаций
animation = 0


# функция выхода из игры
def terminate():
    pygame.quit()
    sys.exit()


# стартовый экран, из которого можно перейти в настройки и саму игру
def start_screen(level_numb, user_id):
    level_number = level_numb

    # фон стартового экрана
    fon = pygame.transform.scale(load_image('start_fon.png'), (width, height))
    screen.blit(fon, (0, 0))

    # выводим кнопки настроек и играть на экран
    screen.blit(buttons['settings_btn'], (750, 0))
    screen.blit(buttons['play_btn'], (170, 240))

    pygame.mixer.music.set_volume(music_level)

    # цикл стартового экрана
    while True:
        for event in pygame.event.get():
            # screen.blit(cursor_img, coord)
            if event.type == pygame.QUIT:
                # выходим из игры, если пользователь закрыл программу
                terminate()
            if event.type == pygame.MOUSEMOTION:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                # проверяем, куда нажал пользователь
                if 750 <= event.pos[0] <= 800 and 0 <= event.pos[1] <= 50:
                    # проигрываем звук нажатия кнопки
                    menu_up.set_volume(sound_effects_level)
                    menu_up.play()
                    settings_screen(level_numb, user_id)
                elif 130 <= event.pos[0] <= 630 and 200 <= event.pos[1] <= 575:
                    # проигрываем звук нажатия кнопки
                    menu_up.set_volume(sound_effects_level)
                    menu_up.play()
                    main_screen(level_number, user_id)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            settings_screen(level_numb, user_id)
        # обновляем экран
        pygame.display.flip()
        clock.tick(FPS)


# экран настроек, в котором можно изменить громкость музыки и звуковых эффектов
def settings_screen(level_num, user_id, in_game=False):
    # глобализируем переменные
    global music_level, sound_effects_level

    # загружаем задний фон
    fon = pygame.transform.scale(load_image('settings_fon.png'), (width, height))
    screen.blit(fon, (0, 0))

    # выводим все кнопки
    screen.blit(buttons['home_btn'], (748, 2))
    screen.blit(buttons['minus_btn'], (450, 210))
    screen.blit(buttons['plus_btn'], (270, 210))
    screen.blit(buttons['minus_btn'], (450, 345))
    screen.blit(buttons['plus_btn'], (270, 345))
    # если пользователь, вышел из игры в настройки,
    # то есть возможность вернуться назад с помощью одной кнопки "return"
    if in_game:
        screen.blit(buttons['return_btn'], (2, 2))

    # цикл экрана настроек
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # выходим из игры, если пользователь закрыл программу
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # проверяем, куда нажал пользователь
                if 748 <= event.pos[0] <= 800 and 0 <= event.pos[1] <= 50:
                    # проигрываем звук нажатия кнопки
                    menu_up.set_volume(sound_effects_level)
                    menu_up.play()
                    start_screen(level_num, user_id)
                if in_game:
                    if 0 <= event.pos[0] <= 50 and 0 <= event.pos[1] <= 50:
                        # проигрываем звук нажатия кнопки
                        menu_up.set_volume(sound_effects_level)
                        menu_up.play()
                        main_screen(level_num, user_id)
                # если это одна из кнопок изменения звука,
                # то изменяем переменные music_level или sound_effects_level соответственно нажатой кнопки
                if 450 <= event.pos[0] <= 500 and 210 <= event.pos[1] <= 260:
                    if music_level >= 0.1:
                        music_level -= 0.1
                    pygame.mixer.music.set_volume(music_level)
                if 270 <= event.pos[0] <= 320 and 210 <= event.pos[1] <= 260:
                    if music_level < 1:
                        music_level += 0.1
                    pygame.mixer.music.set_volume(music_level)
                if 450 <= event.pos[0] <= 500 and 345 <= event.pos[1] <= 395:
                    if sound_effects_level >= 0.1:
                        sound_effects_level -= 0.1
                if 270 <= event.pos[0] <= 320 and 345 <= event.pos[1] <= 395:
                    if sound_effects_level < 1:
                        sound_effects_level += 0.1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            if in_game:
                main_screen(level_num, user_id)
            else:
                start_screen(level_num, user_id)
        # обновляем экран
        pygame.display.flip()
        clock.tick(FPS)


# функция экрана поражения
def lose_screen(level_num, user_id):
    global x_coord, y_coord, jump, jump_height
    # загружаем фон
    fon = pygame.transform.scale(load_image("game_over.png"), (width, height))
    screen.blit(buttons['previous_btn'], (210, 490))
    screen.blit(buttons['home_btn'], (550, 490))
    screen.blit(fon, (0, 0))
    # включаем музыку поражения
    pygame.mixer.music.pause()
    lose_sound.set_volume(music_level)
    lose_sound.play()
    # меняем координаты игрока на дефолтные
    x_coord = 100
    y_coord = 150
    jump = False
    jump_height = 10
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # При нажатии кнокпки повтор, уровень загрузится заново
                if 210 <= event.pos[0] <= 260 and 490 <= event.pos[1] <= 540:
                    # проигрываем звук нажатия кнопки
                    menu_up.set_volume(sound_effects_level)
                    menu_up.play()
                    # продолжаем играть музыку
                    lose_sound.stop()
                    pygame.mixer.music.unpause()
                    main_screen(level_num, user_id)
                    return
                # При нажатии кнопки домой, появиться стартовый экран
                elif 550 <= event.pos[0] <= 600 and 490 <= event.pos[1] <= 540:
                    # проигрываем звук нажатия кнопки
                    menu_up.set_volume(sound_effects_level)
                    menu_up.play()
                    # продолжаем играть музыку
                    pygame.mixer.music.unpause()
                    start_screen(level_num, user_id)
                    return
        pygame.display.flip()
        clock.tick(FPS)


# функция экрана победы
def win_screen(level_num, user_id):
    # увеличиваем уровень
    level_number = level_num
    level_number += 1
    if level_number > 5:
        level_number -= 1

    # вносим изменения в базу данных
    con = sqlite3.connect("users.db")
    cursor = con.cursor()
    cursor.execute(f'UPDATE sums SET level_number = {level_number} WHERE user_id = {user_id};')
    # cохраняем таблицу
    con.commit()

    # очищаем карту
    all_sprites.empty()
    tiles_group.empty()
    thorns_group.empty()
    water_group.empty()
    player_group.empty()
    buttons_group.empty()
    finish_group.empty()

    # загружаем фон
    fon = pygame.transform.scale(load_image("victory.png"), (width, height))
    screen.blit(buttons['next_btn'], (515, 430))
    screen.blit(buttons['previous_btn'], (215, 430))
    screen.blit(fon, (0, 0))

    # включаем музыку победы
    pygame.mixer.music.pause()
    win_sound.set_volume(music_level)
    win_sound.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # При нажатии кнопки повтор, уровень загрузится заново
                if 215 <= event.pos[0] <= 265 and 430 <= event.pos[1] <= 480:
                    # проигрываем звук нажатия кнопки
                    menu_up.set_volume(sound_effects_level)
                    menu_up.play()
                    # продолжаем играть музыку
                    win_sound.stop()
                    pygame.mixer.music.unpause()
                    # возвращаем прошлый уровень
                    level_number -= 1
                    main_screen(level_number, user_id)
                    return
                # При нажатии кнопки далее загрузится следующий уровень
                elif 515 <= event.pos[0] <= 565 and 430 <= event.pos[1] <= 480:
                    main_screen(level_number, user_id)
        pygame.display.flip()
        clock.tick(FPS)


# класс других спрайтов
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, x, y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(x, y)


# класс препятствий
class Thorns(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(thorns_group, all_sprites)
        self.image = tile_images['thorn']
        self.rect = self.image.get_rect().move(x, y)


# класс лавы
class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(thorns_group, all_sprites)
        self.image = tile_images['waterblock']
        self.rect = self.image.get_rect().move(x, y)


# класс элемента финиша
class Finish(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(finish_group, all_sprites)
        self.image = tile_images['finish_flag']
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
    def __init__(self, x_coord, y_coord, level_num, user_id):
        super().__init__(player_group, all_sprites)
        self.image = defoltplace
        self.rect = self.image.get_rect().move(x_coord, y_coord)
        self.level_num = level_num
        self.user_id = user_id

    # функция отвечающая за передвижения персонажа
    def update(self, x_coord, y_coord, jump):
        global animation, left, right, jump_height, is_flying
        # если игрок сталкивается с шипами, то появляется экран поражения
        if pygame.sprite.spritecollideany(self, thorns_group):
            self.kill()
            lose_screen(self.level_num, self.user_id)
        # если игрок сталкивается с лавой, то появляется экран поражения
        if pygame.sprite.spritecollideany(self, water_group):
            self.kill()
            lose_screen(self.level_num, self.user_id)
        # если игрок сталкивается со звездой, то появляется экран победы
        if pygame.sprite.spritecollideany(self, finish_group):
            self.kill()
            win_screen(self.level_num, self.user_id)
        # если игрок провалится, то также появляется экран поражения
        if y_coord > 600:
            self.kill()
            lose_screen(self.level_num, self.user_id)
        # игрок падает, не столкнётся с блоком
        if pygame.sprite.spritecollideany(self, tiles_group) is None and not jump:
            is_flying = True
        if pygame.sprite.spritecollideany(self, tiles_group):
            rect = pygame.sprite.spritecollideany(self, tiles_group).rect
            if rect[0] - x_coord >= 40:
                is_flying = True
        # игрок летит с анимацией падения
        if is_flying:
            self.image = fly[0]
            self.rect = self.image.get_rect().move(x_coord, y_coord)
            return
        if pygame.sprite.spritecollideany(self, tiles_group) or jump:
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
                self.image = fly[0]
                self.rect = self.image.get_rect().move(x_coord, y_coord)
                animation += 1
            else:
                # иначе изначальное положение персонажа
                self.image = defoltplace
                self.rect = self.image.get_rect().move(x_coord, y_coord)


# класс камеры
class Camera(object):
    def __init__(self, camera, width, height):
        self.camera = camera
        self.rect = pygame.Rect(0, 0, width, height)

    # обновляем каждый спрайт
    def apply(self, obj):
        return obj.rect.move(self.rect.topleft)

    # обновляем по отношению к игроку
    def update(self, target):
        self.rect = self.camera(self.rect, target.rect)


# функция конфигурации камеры
def camera_configure(camera, obj):
    width_of_obj, height_of_obj, _, _ = obj
    _, _, w, h = camera
    width_of_obj, height_of_obj = -width_of_obj + 800 / 2, -height_of_obj + 600 / 2

    width_of_obj = min(0, width_of_obj)
    width_of_obj = max(-(camera.width - 800), width_of_obj)
    height_of_obj = max(-(camera.height - 600), height_of_obj)
    height_of_obj = min(0, height_of_obj)

    return pygame.Rect(width_of_obj, height_of_obj, w, h)


# функция генерации уровня с .txt файла
def generate_level(finish_map):
    # инициализируем переменные
    global x_coord, y_coord

    # загружаем карту
    for y in range(len(finish_map)):
        for x in range(len(finish_map[y])):
            if finish_map[y][x] == '@':
                x_coord = x * 50
                y_coord = y * 50
            elif finish_map[y][x] == '#':
                Tile('block', x * 50, y * 20)
            elif finish_map[y][x] == '%':
                Thorns(x * 50, y * 20 - 11)
            elif finish_map[y][x] == '*':
                Tile('clearblock', x * 50, y * 20)
            elif finish_map[y][x] == '$':
                Water(x * 50, y * 20)
            elif finish_map[y][x] == '!':
                Finish(x * 50, y * 20 - 35)


# главный экран
def main_screen(level_num, user_id):
    # глобализируем переменные
    global jump, jump_height, x_coord, y_coord, left, right, animation, is_flying

    # загружаем фон
    fon_image = pygame.transform.scale(load_image('main_fon.png'), (width, height))
    screen.blit(fon_image, (0, 0))

    # выводим кнопки настроек и возращения на стартовый экран
    buttons_class = Buttons()
    buttons_class.draw(screen)

    # переменные для игрока
    x_coord = 50
    y_coord = 100
    speed = 5
    jump = False
    jump_height = 10
    is_flying = True
    left = False
    right = False
    animation = 0
    level_number = level_num

    # выводим на экран игрока
    player = Player(x_coord, y_coord, level_num, user_id)

    # инициализируем камеру
    camera = Camera(camera_configure, 1600, 600)

    # выводим спрайты
    level_name = f'level{level_number}.txt'
    finish_map = load_level(level_name)
    generate_level(finish_map)

    # цикл главного экрана
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # выходим из игры, если пользователь закрыл программу
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # проверяем, куда нажал пользователь
                if 750 <= event.pos[0] <= 800 and 0 <= event.pos[1] <= 50:
                    # проигрываем звук нажатия кнопки
                    menu_up.set_volume(sound_effects_level)
                    menu_up.play()
                    player.kill()
                    settings_screen(level_number, True)
                elif 0 <= event.pos[0] <= 50 and 0 <= event.pos[1] <= 50:
                    # проигрываем звук нажатия кнопки
                    menu_up.set_volume(sound_effects_level)
                    menu_up.play()
                    player.kill()
                    start_screen(level_number, user_id)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            # выход в настройки клавишей ESCAPE
            player.kill()
            settings_screen(level_number, True)
        if keys[pygame.K_LEFT] and x_coord > 5:
            x_coord -= speed
            left = True
            right = False
        elif keys[pygame.K_RIGHT] and x_coord < 1600 - width_of_player - 5:
            # бег при нажатии кнопки вправо
            x_coord += speed
            left = False
            right = True
        else:
            # игрок стоит на месте
            left = False
            right = False
            animation = 0
        if not jump:
            # если персонаж не в прыжке, возможность прыжка кнопкой вверх
            if keys[pygame.K_UP]:
                if pygame.sprite.spritecollideany(player, tiles_group):
                    jump = True
                else:
                    jump = False
        if jump:
            # скорость падения, высота прыжка и момент остановки прыжка
            if jump_height >= 0:
                y_coord -= (jump_height ** 2) / 2
                jump_height -= 1
            if jump_height < 0:
                if pygame.sprite.spritecollideany(player, tiles_group):
                    # игрок столкнулся с другим спрайтом
                    drop.set_volume(sound_effects_level)
                    drop.play()
                    y_coord = pygame.sprite.spritecollideany(player, tiles_group).rect[1] - width_of_player - 6
                    jump = False
                    jump_height = 10
                else:
                    y_coord += (jump_height ** 2) / 2
                    jump_height -= 1
        # падение игрока
        if is_flying:
            if pygame.sprite.spritecollideany(player, tiles_group):
                # если столкнулся с землёй, то оставляем его там
                y_coord = pygame.sprite.spritecollideany(player, tiles_group).rect[1] - width_of_player - 6
                drop.set_volume(sound_effects_level)
                drop.play()
                jump_height = 10
                is_flying = False
            else:
                # в противном случае игрок летит дальше
                y_coord += (jump_height ** 2) / 2
                jump_height -= 1
                is_flying = True
        # обновляем экран
        screen.blit(fon_image, (0, 0))
        all_sprites.update(x_coord, y_coord, jump)
        # обновляем камеру
        camera.update(player)
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))
        # рисуем кнопки
        buttons_class.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


# Окно входа в аккаунт
class Login_window(PyQt5.QtWidgets.QDialog):
    global level_number

    def __init__(self):
        super().__init__()
        self.widget = None
        uic.loadUi('login_qt.ui', self)
        self.setWindowTitle('Вход/регистрация в аккаунт')
        self.setFixedSize(self.size())

        # Скрытие строки с паролем
        self.password.setEchoMode(2)

        # Обработка кнопок входа и регистрации
        self.login_button.clicked.connect(self.login_in)
        self.sign_up_button.clicked.connect(self.sign_up)

    # Функция открытия главного окна
    def game_starting(self, level_num, user_id):
        Login_window.close(self)
        level_number = level_num[0][0]
        start_screen(level_number, user_id)

    # Функция входа в аккаунт
    def login_in(self):
        # Подключение к базе данных users.db
        con = sqlite3.connect("users.db")
        cursor = con.cursor()
        # Считывание логина и пароля
        login = self.login.text()
        password = self.password.text()
        # Проверка введены ли логин и пароль
        if not login or not password:
            QMessageBox.critical(self, 'Ошибка!', 'Вы заполнили не все поля!', QMessageBox.Ok)
        else:
            # Хеширование пароля с помощью библиотеки hashlib
            password = bytes(password, 'utf-8')
            hash_password = hashlib.sha1(password).hexdigest()
            # Ищем пользователя в таблице users в базе данных
            result_of_execute = cursor.execute('SELECT login, password FROM user WHERE login = ? AND password = ?',
                                               (login, hash_password))
            # Проверка - найден ли пользователь
            if result_of_execute.fetchall():
                # Если да, выводим стартовый экран
                user_id = cursor.execute('SELECT id FROM user WHERE login = ? AND password = ?',
                                         (login, hash_password)).fetchall()
                level_num = cursor.execute(f'SELECT level_number FROM sums WHERE user_id = {user_id[0][0]}').fetchall()
                # Открываем стартовый экран и передаём текущий уровень
                self.game_starting(level_num, user_id[0][0])
            else:
                # В противном случае выносим окно с ошибкой
                return QMessageBox.information(self, 'Внимание!', 'Неправильное имя пользователя или пароль')

    # Функция регистрации в аккаунт
    def sign_up(self):
        # Подключение к базе данных data.db
        con = sqlite3.connect("users.db")
        cursor = con.cursor()
        # Считывание логина и пароля
        login = self.login.text()
        password = self.password.text()
        # Проверка введены ли логин и пароль
        if not login or not password:
            QMessageBox.critical(self, 'Ошибка!', 'Вы заполнили не все поля!', QMessageBox.Ok)
        else:
            # Хеширование пароля с помощью библиотеки hashlib
            password = bytes(password, 'utf-8')
            hash_password = hashlib.sha1(password).hexdigest()
            # Проверяем нет ли пользователя в базе данных
            if_user_exist = cursor.execute(f'SELECT * FROM user WHERE login = {login}')
            if if_user_exist.fetchall():
                # Если пользователь с таким логином уже существует, то выносим окно с ошибкой
                QMessageBox.critical(self, 'Внимание!', 'Пользователь с таким логином уже зарегистрирован.',
                                     QMessageBox.Ok)
            else:
                # Если пользователя, нет заносим его в базу данных
                cursor.execute(f'INSERT INTO user(login,password) VALUES("{login}", "{hash_password}")')
                # Сохраняем таблицу
                con.commit()
                user_id = cursor.execute("SELECT id FROM user WHERE login = ? AND password = ?",
                                         (login, hash_password)).fetchall()
                cursor.execute(f'INSERT INTO sums(user_id) VALUES({user_id[0][0]})')
                # выводим стартовый экран
                # Сохраняем таблицу
                con.commit()
                self.game_starting(1, user_id[0][0])


# Запуск программы
if __name__ == '__main__':
    app = QApplication(sys.argv)
    pass_dialog = Login_window()
    pass_dialog.show()
    sys.exit(app.exec_())
