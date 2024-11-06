import pygame
import random
import os

class Config:
    def __init__(self):
        self.window_size = (1920, 1080)
        self.cell_size = 20
        self.font_size = int(self.cell_size * 0.8)
        self.cols = self.window_size[0] // self.cell_size
        self.rows = self.window_size[1] // self.cell_size
        self.matrix_chars = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃ1234567890"
        self.colors = {
            'green': (0, 255, 0),
            'background': (0, 0, 0)
        }

class Cell:
    def __init__(self, config):
        # 30% шанс живой клетки при создании
        self.alive = random.random() > 0.7
        self.char = random.choice(config.matrix_chars)
        self.brightness = random.randint(230, 255) if self.alive else 0

class MatrixGame:
    def __init__(self, config, screen, font):
        self.config = config
        self.screen = screen
        self.font = font
        self.reset()
        
    def reset(self):
        self.grid = [[Cell(self.config) for _ in range(self.config.cols)] 
                    for _ in range(self.config.rows)]
        self.generation = 0
        self.last_reset = 0
        
    def count_alive_cells(self):
        return sum(cell.alive for row in self.grid for cell in row)
    
    def add_random_cells(self):
        if self.generation % 200 == 0:
            for _ in range(self.config.rows * self.config.cols // 100):
                row = random.randrange(self.config.rows)
                col = random.randrange(self.config.cols)
                cell = self.grid[row][col]
                if not cell.alive:
                    cell.alive = True
                    cell.brightness = 255
                    cell.char = random.choice(self.config.matrix_chars)
    
    def check_and_reset(self):
        # Перезапуск если живых клеток меньше 5%
        if self.generation - self.last_reset > 100:
            alive_cells = self.count_alive_cells()
            if alive_cells < (self.config.rows * self.config.cols * 0.05):
                self.reset()
            self.last_reset = self.generation

    def count_neighbors(self, row, col):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                r = (row + i) % self.config.rows
                c = (col + j) % self.config.cols
                if self.grid[r][c].alive:
                    count += 1
        return count

    def update(self):
        self.generation += 1
        self.add_random_cells()
        self.check_and_reset()
        
        new_states = [[False for _ in range(self.config.cols)] 
                     for _ in range(self.config.rows)]
        
        # Правила игры "Жизнь": 2-3 соседа для выживания, 3 для рождения
        for row in range(self.config.rows):
            for col in range(self.config.cols):
                neighbors = self.count_neighbors(row, col)
                cell = self.grid[row][col]
                
                if cell.alive:
                    new_states[row][col] = (2 <= neighbors <= 3)
                else:
                    new_states[row][col] = (neighbors == 3)
        
        for row in range(self.config.rows):
            for col in range(self.config.cols):
                cell = self.grid[row][col]
                new_state = new_states[row][col]
                
                if new_state != cell.alive:
                    if new_state:
                        cell.alive = True
                        cell.brightness = random.randint(230, 255)
                        cell.char = random.choice(self.config.matrix_chars)
                    else:
                        cell.alive = False
                        cell.brightness = max(cell.brightness, 100)

    def draw(self):
        self.screen.fill(self.config.colors['background'])
        
        for row in range(self.config.rows):
            for col in range(self.config.cols):
                cell = self.grid[row][col]
                if cell.brightness > 0:
                    if cell.alive and cell.brightness < 230:
                        cell.brightness = random.randint(230, 255)
                    
                    color = (0, cell.brightness, 0)
                    text = self.font.render(cell.char, True, color)
                    self.screen.blit(
                        text, 
                        (col * self.config.cell_size, row * self.config.cell_size)
                    )
                    
                    if not cell.alive:
                        cell.brightness = max(0, cell.brightness - 5)

def main():
    config = Config()
    
    pygame.init()
    screen = pygame.display.set_mode(config.window_size, pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    
    font_path = os.path.join(os.path.dirname(__file__), 'font', 'msmincho.ttc')
    font = pygame.font.Font(font_path, config.font_size)
    
    game = MatrixGame(config, screen, font)
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    game.reset()
                    
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == '__main__':
    main()