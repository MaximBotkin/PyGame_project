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
def load_level(filename="level1.txt"):
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


# передаем изображения всех кнопок в словарь
buttons = {'home_btn': load_image("home_button.png"), 'minus_btn': load_image("minus.png"),
           'plus_btn': load_image("plus.png"), 'mute_btn': load_image("mute.png"),
           'settings_btn': load_image("settings_button.png"), 'unmute_btn': load_image("unmute.png"),
           'play_btn': load_image("play_button.png"), 'return_btn': load_image("return_button.png")}


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
            if event.type == pygame.QUIT:
                # выходим из игры, если пользователь закрыл программу
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
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

# загружаем карту
level_map = load_level()
# загружаем изображения самой игры
tile_images = {
    'thorn': load_image('thorns.png'),
    'block': load_image("block.png"),
    'player': load_image("player1.jpg")
}


# главный экран
def main_screen():
    # загружаем фон
    fon_image = pygame.transform.scale(load_image('main_fon.png'), (width, height))
    screen.blit(fon_image, (0, 0))

    # выводим кнопки настроек и возращения на стартовый экран
    screen.blit(buttons['settings_btn'], (750, 0))
    screen.blit(buttons['home_btn'], (2, 2))

    # цикл главного экрана
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # выходим из игры, если пользователь закрыл программу
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                # проверяем, куда нажал пользователь
                if 750 <= event.pos[0] <= 800 and 0 <= event.pos[1] <= 50:
                    settings_screen(True)
                elif 0 <= event.pos[0] <= 50 and 0 <= event.pos[1] <= 50:
                    start_screen()
        # обновляем экран
        pygame.display.update()
        clock.tick(FPS)
        pygame.display.flip()


# открываем игру с главного экрана
if __name__ == '__main__':
    start_screen()
