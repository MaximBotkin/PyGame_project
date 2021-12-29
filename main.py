import pygame
import sys
import os

pygame.init()
width, height = 800, 600
size = width, height
screen = pygame.display.set_mode(size)

FPS = 60
clock = pygame.time.Clock()

music_level = 0.5
sound_effects_level = 0.5
pygame.mixer.music.load('data/sound_effects/music.wav')
pygame.mixer.music.set_volume(music_level)
pygame.mixer.music.play(loops=-1)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Ошибка загрузки файла')
        raise SystemExit(message)
    if colorkey:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename="level1.txt"):
    filename = "levels/" + filename
    with open(filename, 'r') as map_file:
        level = [line.strip() for line in map_file]
    finish_map = []
    for st in level:
        a = []
        for elem in st:
            a.append(elem)
        finish_map.append(a)
    return finish_map


buttons = {'home_btn': load_image("home_button.png"), 'minus_btn': load_image("minus.png"),
           'plus_btn': load_image("plus.png"), 'mute_btn': load_image("mute.png"),
           'settings_btn': load_image("settings_button.png"), 'unmute_btn': load_image("unmute.png"),
           'play_btn': load_image("play_button.png"), 'return_btn': load_image("return_button.png")}


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ['Pygame Project', 'Перед началом игры ознакомьтесь с файлом read_before_play.txt,',
                  'который лежит в папке с вашей программой.']
    fon = pygame.transform.scale(load_image('start_fon.png'), (width, height))
    screen.blit(fon, (0, 0))

    font_for_title = pygame.font.Font(None, 60)
    string_rendered = font_for_title.render(intro_text[0], 1, pygame.Color((127, 0, 255)))
    screen.blit(string_rendered, (242, 50))
    font_about = pygame.font.Font(None, 30)
    string_about1 = font_about.render(intro_text[1], 1, pygame.Color((127, 0, 255)))
    screen.blit(string_about1, (20, 150))
    string_about2 = font_about.render(intro_text[2], 1, pygame.Color((127, 0, 255)))
    screen.blit(string_about2, (20, 175))

    screen.blit(buttons['settings_btn'], (750, 0))

    screen.blit(buttons['play_btn'], (130, 200))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 750 <= event.pos[0] <= 800 and 0 <= event.pos[1] <= 50:
                    settings_screen()
                elif 130 <= event.pos[0] <= 630 and 200 <= event.pos[1] <= 575:
                    main_screen()
        pygame.display.flip()
        clock.tick(FPS)


def settings_screen(in_game=False):
    global music_level, sound_effects_level
    fon = pygame.transform.scale(load_image('settings_fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))

    screen.blit(buttons['home_btn'], (748, 2))
    screen.blit(buttons['minus_btn'], (450, 150))
    screen.blit(buttons['plus_btn'], (270, 150))
    screen.blit(buttons['minus_btn'], (450, 350))
    screen.blit(buttons['plus_btn'], (270, 350))
    if in_game:
        screen.blit(buttons['return_btn'], (2, 2))
    text = ['Громкость музыки', 'Громкость звуковых эффектов']
    font_for_title = pygame.font.Font(None, 50)
    string_1 = font_for_title.render(text[0], 1, pygame.Color((127, 0, 255)))
    screen.blit(string_1, (242, 100))
    string_2 = font_for_title.render(text[1], 1, pygame.Color((127, 0, 255)))
    screen.blit(string_2, (130, 300))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 748 <= event.pos[0] <= 800 and 0 <= event.pos[1] <= 50:
                    start_screen()
                if in_game:
                    if 0 <= event.pos[0] <= 50 and 0 <= event.pos[1] <= 50:
                        main_screen()
                if 450 <= event.pos[0] <= 514 and 150 <= event.pos[1] <= 214:
                    music_level -= 0.1
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(loops=-1)
                if 270 <= event.pos[0] <= 334 and 150 <= event.pos[1] <= 214:
                    music_level += 0.1
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(loops=-1)
        pygame.display.flip()
        clock.tick(FPS)


level_map = load_level()
tile_images = {
    'thorn': load_image('thorns.png'),
    'block': load_image("block.png"),
    'player': load_image("player1.jpg")
}


def main_screen():
    running = True

    fon_image = pygame.transform.scale(load_image('main_fon.png'), (width, height))
    screen.blit(fon_image, (0, 0))

    screen.blit(buttons['settings_btn'], (750, 0))
    screen.blit(buttons['home_btn'], (2, 2))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                if 750 <= event.pos[0] <= 800 and 0 <= event.pos[1] <= 50:
                    settings_screen(True)
                elif 0 <= event.pos[0] <= 50 and 0 <= event.pos[1] <= 50:
                    start_screen()
        pygame.display.update()
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    start_screen()
