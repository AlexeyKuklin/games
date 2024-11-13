import pygame
import math
import time
import random
from falling_text import FallingText

class Game:
    def __init__(self, window_size, game_font, result_font, result_big_font, sounds):
        self.window_size = window_size
        self.game_font = game_font
        self.result_font = result_font
        self.result_big_font = result_big_font
        self.sounds = sounds
        
        self.cell_size = window_size[0] // 3
        self.board = None
        self.ai = None
        
        self.GREEN = (0, 255, 0)
        self.BRIGHT_GREEN = (50, 255, 50)
        
        # Состояния AI
        self.AI_THINKING = 1
        self.AI_MOVING = 2
        self.ai_state = None
        self.ai_move = None
        self.ai_start_time = 0
        self.ai_animation_progress = 0
        
        self.game_over = False
        self.game_over_start = 0
        # Список падающих символов: [x, y, speed, symbol, rotation, rotation_speed]
        self.falling_symbols = []
        
        self.symbols_flash = {}  # Словарь для хранения состояния вспышки символов
        self.flash_duration = 1.0  # Увеличили длительность вспышки до 1 секунды
        
        self.result_text = None  # Добавляем для хранения падающих букв заставки
        self.falling_letters = []  # Для букв заставки
        
        self.is_resetting = False  # Флаг для анимации исчезновения
        self.reset_start_time = 0  # Время начала сброса
        
        self.falling_texts = []  # Список для хранения падающих текстов
        
        self.score_x = 0  # Счет игрока
        self.score_o = 0  # Счет компьютера
        self.score_draw = 0  # Добавляем счетчик ничьих
        
        self.reset_game()
        
    def reset_game(self):
        from board import Board
        from ai import AI
        
        self.board = Board()
        self.ai = AI()
        self.game_over = False
        self.ai_state = None
        self.ai_move = None
        self.ai_animation_progress = 0
        
    def start_game_over_animation(self):
        self.game_over = True
        self.game_over_start = time.time()
        self.falling_symbols = []
        self.falling_letters = []
        
        # Обновляем счет
        if self.board.is_winner('X'):
            self.score_x += 1
            self.result_text = "ПОБЕДА"
        elif self.board.is_winner('O'):
            self.score_o += 1
            self.result_text = "ПОРАЖЕНИЕ"
        else:
            self.score_draw += 1  # Увеличиваем счетчик ничьих
            self.result_text = "НИЧЬЯ"
        
        # Создаем падающие символы только для игрового поля
        for row in range(3):
            for col in range(3):
                if self.board.board[row][col] != ' ':
                    x = col * self.cell_size + self.cell_size // 2
                    y = row * self.cell_size + self.cell_size // 2
                    self.falling_symbols.append([
                        x,  # x position
                        y,  # y position
                        random.uniform(2, 5),  # fall speed
                        self.board.board[row][col],  # symbol
                        random.uniform(-0.5, 0.5),  # rotation
                        random.uniform(-0.1, 0.1)  # rotation speed
                    ])
    
    def start_result_falling(self):
        self.is_resetting = True
        self.reset_start_time = time.time()
        
        # Создаем падающий текст результата (обновили озицию)
        result_pos = (self.window_size[0]//2, self.window_size[1]//2 + 40)
        self.falling_texts.append(
            FallingText(self.result_text, self.result_big_font, result_pos)
        )
        
        # Создаем падающий текст подсказки (обновили позицию)
        restart_pos = (self.window_size[0]//2, self.window_size[1]//2 + 100)
        self.falling_texts.append(
            FallingText("ПРОБЕЛ - РЕСТАРТ", self.result_font, restart_pos)
        )
    
    def handle_event(self, event, current_time):
        if self.game_over and not self.is_resetting:
            # Начать новую игру можно пробелом или левым кликом
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or \
               (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                self.start_result_falling()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over and self.ai_state is None:
            cell = self.get_cell_from_mouse(event.pos)
            if cell and self.board.make_move(*cell):
                self.play_sound('click')
                if self.board.is_game_over():
                    self.start_game_over_animation()
                    if self.board.is_winner('X'):
                        self.play_sound('win')
                    elif self.board.is_winner('O'):
                        self.play_sound('lose')
                    else:
                        self.play_sound('draw')
                else:
                    self.ai_state = self.AI_THINKING
                    self.ai_start_time = current_time
    
    def update(self, current_time):
        if self.ai_state == self.AI_THINKING and current_time - self.ai_start_time > 0.2:
            # Получаем ход от AI
            best_move = self.ai.get_best_move(self.board)
            
            # С вероятностью 1/15 делаем случайный ход вместо лучшего
            if random.randint(1, 15) == 1:
                empty_cells = self.board.get_empty_cells()
                if empty_cells:  # Проверяем, что есть доступные ходы
                    self.ai_move = random.choice(empty_cells)
                else:
                    self.ai_move = best_move
            else:
                self.ai_move = best_move
            
            self.ai_state = self.AI_MOVING
            self.ai_start_time = current_time
            self.ai_animation_progress = 0
            
        elif self.ai_state == self.AI_MOVING:
            self.ai_animation_progress = min(1, (current_time - self.ai_start_time) * 4)
            
            if self.ai_animation_progress >= 1:
                self.board.make_move(*self.ai_move)
                self.play_sound('move')
                if self.board.is_game_over():
                    self.start_game_over_animation()
                    if self.board.is_winner('O'):
                        self.play_sound('lose')
                    elif self.board.is_winner('X'):
                        self.play_sound('win')
                    else:
                        self.play_sound('draw')
                self.ai_state = None
                self.ai_move = None
        
        # Обновляем падающие символы и буквы
        if self.game_over:
            if self.falling_symbols:
                for symbol in self.falling_symbols:
                    symbol[1] += symbol[2]  # Update y position
                    symbol[4] += symbol[5]  # Update rotation
                
                self.falling_symbols = [s for s in self.falling_symbols if s[1] < self.window_size[1] + 50]
            
            if self.falling_letters:
                for letter in self.falling_letters:
                    letter[1] += letter[2]  # Update y position
                    letter[4] += letter[5]  # Update rotation
                    letter[6] = max(0, letter[6] - 2)  # Уменьшаем позрачность
                
                self.falling_letters = [l for l in self.falling_letters if l[1] < self.window_size[1] + 50 and l[6] > 0]
        
        # Обновляем падающие тексты
        if self.falling_texts:
            for text in self.falling_texts:
                text.update()
            self.falling_texts = [t for t in self.falling_texts if not t.is_finished()]
            
            # Проверяем завершение анимации
            if not self.falling_texts and self.is_resetting:
                self.is_resetting = False
                self.reset_game()
    
    def draw(self, screen):
        self.draw_grid(screen)
        self.draw_board(screen)
        if self.game_over:
            self.draw_result(screen)
            
    def draw_grid(self, screen):
        for i in range(1, 3):
            pygame.draw.line(screen, self.GREEN, 
                           (i * self.cell_size, 0),
                           (i * self.cell_size, self.window_size[1]), 3)
            pygame.draw.line(screen, self.GREEN,
                           (0, i * self.cell_size),
                           (self.window_size[0], i * self.cell_size), 3)
                           
    def draw_board(self, screen):
        current_time = time.time()
        
        if self.game_over:
            for x, y, _, symbol, rotation, _ in self.falling_symbols:
                # Создаем поверхность для символа
                text = self.game_font.render(symbol, True, (0, 200, 0) if symbol == 'X' else (0, 180, 0))
                glow = self.game_font.render(symbol, True, (0, 100, 0) if symbol == 'X' else (0, 80, 0))
                
                # Поворачиваем символы
                rotated_text = pygame.transform.rotate(text, math.degrees(rotation))
                rotated_glow = pygame.transform.rotate(glow, math.degrees(rotation))
                
                # Рисуем свечение
                for offset in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
                    glow_pos = rotated_glow.get_rect(center=(x + offset[0], y + offset[1]))
                    screen.blit(rotated_glow, glow_pos)
                
                # Рисуем символ
                text_pos = rotated_text.get_rect(center=(x, y))
                screen.blit(rotated_text, text_pos)
            return

        for row in range(3):
            for col in range(3):
                x = col * self.cell_size
                y = row * self.cell_size
                center = (x + self.cell_size//2, y + self.cell_size//2)
                
                symbol = self.board.board[row][col]
                if symbol == ' ':
                    continue
                
                # Получаем время установки символа
                pos_key = (row, col)
                if pos_key not in self.symbols_flash:
                    self.symbols_flash[pos_key] = current_time
                
                # Более простая и чёткая вспышка
                flash_time = current_time - self.symbols_flash[pos_key]
                flash_progress = min(flash_time / self.flash_duration, 1.0)
                
                # Простое линейное затухание с быстрым стартом
                flash_factor = max(0, 1 - flash_progress * 2) if flash_progress < 0.5 else 0
                
                # Базовая и максимальная яркость
                base_intensity = 180 if symbol == 'O' else 200
                flash_intensity = 255
                
                # Текущая яркость
                current_intensity = int(base_intensity + (flash_intensity - base_intensity) * flash_factor)
                
                if symbol == 'X':
                    # Основное свечение
                    glow_intensity = int(current_intensity * 0.6)
                    glow = self.game_font.render('X', True, (0, glow_intensity, 0))
                    
                    # Простое дополнительное свечение только в момент вспышки
                    if flash_factor > 0:
                        for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
                            glow_pos = glow.get_rect(center=(center[0] + offset[0], center[1] + offset[1]))
                            screen.blit(glow, glow_pos)
                    
                    # Обычное свечение
                    for offset in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
                        glow_pos = glow.get_rect(center=(center[0] + offset[0], center[1] + offset[1]))
                        screen.blit(glow, glow_pos)
                    
                    # Основной символ
                    text = self.game_font.render('X', True, (0, current_intensity, 0))
                    screen.blit(text, text.get_rect(center=center))
                    
                elif symbol == 'O':
                    if (row, col) == self.ai_move and self.ai_state == self.AI_MOVING:
                        # Анимация появления O
                        offset = int(math.sin(self.ai_animation_progress * math.pi) * 20)
                        alpha = int(255 * min(1, self.ai_animation_progress * 2))
                        
                        glow_intensity = max(60, int(current_intensity * 0.4))
                        glow = self.game_font.render('O', True, (0, glow_intensity, 0))
                        glow.set_alpha(alpha)
                        for offset_xy in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
                            glow_pos = glow.get_rect(center=(center[0] + offset_xy[0], 
                                                           center[1] + offset_xy[1] - offset))
                            screen.blit(glow, glow_pos)
                        
                        text = self.game_font.render('O', True, (0, current_intensity, 0))
                        text.set_alpha(alpha)
                        screen.blit(text, text.get_rect(center=(center[0], center[1] - offset)))
                    else:
                        # Аналогичная логика для O
                        glow_intensity = int(current_intensity * 0.6)
                        glow = self.game_font.render('O', True, (0, glow_intensity, 0))
                        
                        if flash_factor > 0:
                            for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
                                glow_pos = glow.get_rect(center=(center[0] + offset[0], center[1] + offset[1]))
                                screen.blit(glow, glow_pos)
                        
                        for offset in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
                            glow_pos = glow.get_rect(center=(center[0] + offset[0], center[1] + offset[1]))
                            screen.blit(glow, glow_pos)
                        
                        text = self.game_font.render('O', True, (0, current_intensity, 0))
                        screen.blit(text, text.get_rect(center=center))
                        
    def draw_result(self, screen):
        if not self.game_over:
            return
        
        overlay = pygame.Surface(self.window_size)
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        
        # Тексты для счета (все вертикально)
        score_texts = [
            ("ПОБЕДА", self.score_x, True),
            ("НИЧЬЯ", self.score_draw, True),  # Используем счетчик ничьих
            ("ПОРАЖЕНИЕ", self.score_o, True)
        ]
        
        # Позиции для каждого столбца счета
        x_positions = [self.window_size[0]//4, self.window_size[0]//2, 3 * self.window_size[0]//4]
        
        # Рисуем каждый столбец счета
        for (text, value, _), x_pos in zip(score_texts, x_positions):
            y_pos = 60  # Увеличили начальную позицию по Y
            
            # Сначала рисуем значение счета
            value_text = str(value)
            glow_value = self.result_font.render(value_text, True, (0, 80, 0))
            score_value = self.result_font.render(value_text, True, (0, 255, 0))
            
            value_pos = (x_pos, y_pos - 35)  # Увеличили отступ между счетом и текстом
            
            # Рисуем свечение для значения
            for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
                glow_rect = glow_value.get_rect(center=(value_pos[0] + offset[0], value_pos[1] + offset[1]))
                screen.blit(glow_value, glow_rect)
            
            screen.blit(score_value, score_value.get_rect(center=value_pos))
            
            # Затем рисуем текст вертикально
            for i, letter in enumerate(text):
                glow_letter = self.result_font.render(letter, True, (0, 80, 0))
                score_letter = self.result_font.render(letter, True, (0, 255, 0))
                
                letter_pos = (x_pos, y_pos + i * 20)
                
                # Рисуем свечение для буквы
                for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
                    glow_rect = glow_letter.get_rect(center=(letter_pos[0] + offset[0], letter_pos[1] + offset[1]))
                    screen.blit(glow_letter, glow_rect)
                
                screen.blit(score_letter, score_letter.get_rect(center=letter_pos))
        
        # Рисуем падающие тексты
        if self.falling_texts:
            for text in self.falling_texts:
                text.draw(screen)
        # Если нет падающих текстов и не в процессе сброса, показываем статичный текст
        elif not self.is_resetting:
            # Рисуем текст результата (сместили ниже)
            glow_text = self.result_big_font.render(self.result_text, True, (0, 80, 0))
            result_text = self.result_big_font.render(self.result_text, True, (0, 255, 0))
            
            result_pos = (self.window_size[0]//2, self.window_size[1]//2 + 40)  # Сместили вниз
            
            # Рисуем свечение для результата
            for offset in [(3, 3), (-3, -3), (3, -3), (-3, 3), (0, 3), (3, 0), (-3, 0), (0, -3)]:
                glow_result_rect = glow_text.get_rect(
                    center=(result_pos[0] + offset[0], result_pos[1] + offset[1]))
                screen.blit(glow_text, glow_result_rect)
            
            screen.blit(result_text, result_text.get_rect(center=result_pos))
            
            # Рисуем текст "ПРОБЕЛ - РЕСТАРТ" (тоже сместили ниже)
            restart_text = "ПРОБЕЛ - РЕСТАРТ"
            glow_restart = self.result_font.render(restart_text, True, (0, 60, 0))
            restart_text = self.result_font.render(restart_text, True, (0, 180, 0))
            
            restart_pos = (self.window_size[0]//2, self.window_size[1]//2 + 100)  # Сместили вниз
            
            for offset in [(3, 3), (-3, -3), (3, -3), (-3, 3), (0, 3), (3, 0), (-3, 0), (0, -3)]:
                glow_restart_rect = glow_restart.get_rect(
                    center=(restart_pos[0] + offset[0], restart_pos[1] + offset[1]))
                screen.blit(glow_restart, glow_restart_rect)
            
            screen.blit(restart_text, restart_text.get_rect(center=restart_pos))
    
    def get_cell_from_mouse(self, pos):
        x, y = pos
        row = y // self.cell_size
        col = x // self.cell_size
        if 0 <= row < 3 and 0 <= col < 3:
            return int(row), int(col)
        return None 
    
    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()