import pygame
import random
import math

class FallingText:
    def __init__(self, text, font, pos, color=(0, 255, 0)):
        self.text = text
        self.font = font
        self.color = color
        self.letters = []
        
        # Создаем падающие буквы
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=pos)
        
        for i, letter in enumerate(text):
            letter_surface = font.render(letter, True, color)
            letter_width = letter_surface.get_width()
            x = text_rect.left + i * letter_width
            y = text_rect.centery
            
            self.letters.append([
                x,  # x position
                y,  # y position
                random.uniform(1, 3),  # fall speed
                letter,  # symbol
                random.uniform(-0.3, 0.3),  # rotation
                random.uniform(-0.05, 0.05),  # rotation speed
                255  # alpha
            ])
    
    def update(self):
        # Обновляем позиции и прозрачность букв
        for letter in self.letters:
            letter[1] += letter[2]  # Update y position
            letter[4] += letter[5]  # Update rotation
            letter[6] = max(0, letter[6] - 2)  # Уменьшаем прозрачность
        
        # Удаляем невидимые буквы
        self.letters = [l for l in self.letters if l[6] > 0]
    
    def draw(self, screen):
        for x, y, _, letter, rotation, _, alpha in self.letters:
            text = self.font.render(letter, True, self.color)
            text.set_alpha(alpha)
            rotated = pygame.transform.rotate(text, math.degrees(rotation))
            text_rect = rotated.get_rect(center=(x, y))
            screen.blit(rotated, text_rect)
    
    def is_finished(self):
        return len(self.letters) == 0 