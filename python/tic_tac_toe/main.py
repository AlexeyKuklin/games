import pygame
from matrix_effect import MatrixEffect
from game import Game
import time
import os
import sys

def resource_path(relative_path):
    """ Получаем абсолютный путь к ресурсу """
    try:
        # PyInstaller создает временную папку и хранит путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_sounds():
    sounds = {}
    try:
        # Загружаем звуки используя resource_path
        sounds['background'] = pygame.mixer.Sound(resource_path('sound/background.wav'))
        sounds['win'] = pygame.mixer.Sound(resource_path('sound/win.wav'))
        sounds['lose'] = pygame.mixer.Sound(resource_path('sound/lose.wav'))
        sounds['draw'] = pygame.mixer.Sound(resource_path('sound/draw.wav'))
        sounds['click'] = pygame.mixer.Sound(resource_path('sound/click.wav'))
        sounds['move'] = pygame.mixer.Sound(resource_path('sound/move.wav'))
        
        # Настраиваем громкость
        sounds['background'].set_volume(0.2)
        sounds['click'].set_volume(0.3)
        sounds['move'].set_volume(0.3)
        for sound in ['win', 'lose', 'draw']:
            sounds[sound].set_volume(0.4)
            
        # Запускаем фоновую музыку
        sounds['background'].play(-1)
    except Exception as e:
        print(f"Не удалось загрузить звуковые файлы: {e}")
    return sounds

def load_fonts():
    try:
        matrix_font = pygame.font.Font(resource_path("font/msmincho.ttc"), 20)
    except:
        matrix_font = pygame.font.SysFont('msgothic', 20)
    
    game_font = pygame.font.Font(None, 120)
    result_font = pygame.font.Font(None, 42)
    result_big_font = pygame.font.Font(None, 64)
    
    return matrix_font, game_font, result_font, result_big_font

def main():
    pygame.init()
    pygame.mixer.init()

    WINDOW_SIZE = (500, 500)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Крестики-нолики в Матрице")

    # Загружаем ресурсы
    sounds = load_sounds()
    matrix_font, game_font, result_font, result_big_font = load_fonts()

    # Создаем объекты
    matrix = MatrixEffect(WINDOW_SIZE, matrix_font)
    game = Game(WINDOW_SIZE, game_font, result_font, result_big_font, sounds)

    running = True
    clock = pygame.time.Clock()

    while running:
        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.handle_event(event, current_time)
        
        game.update(current_time)
        matrix.update()
        matrix.draw(screen)
        game.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.stop()
    pygame.quit()

if __name__ == '__main__':
    main() 