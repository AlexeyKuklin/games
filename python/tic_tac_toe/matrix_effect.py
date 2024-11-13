import random

class MatrixEffect:
    def __init__(self, window_size, font):
        self.window_size = window_size
        self.font = font
        self.font_size = font.get_height()
        
        self.characters = [chr(i) for i in range(0x30A0, 0x30FF)]
        self.drops = []
        self.init_drops()
        
    def init_drops(self):
        columns = self.window_size[0] // self.font_size
        self.drops = []
        
        for x in range(columns):
            x_pos = x * self.font_size
            
            num_chars = (self.window_size[1] // self.font_size) + 30
            
            drop = {
                'x': x_pos,
                'y': random.randint(-500, 0),
                'speed': random.uniform(0.5, 2.0),
                'chars': [random.choice(self.characters) for _ in range(num_chars)],
                'change_timers': [random.randint(5, 20) for _ in range(num_chars)]
            }
            self.drops.append(drop)
            
    def update(self):
        for drop in self.drops:
            drop['y'] += drop['speed']
            
            if drop['y'] - (len(drop['chars']) * self.font_size) > self.window_size[1]:
                drop['y'] = random.randint(-50, 0)
                drop['speed'] = random.uniform(0.5, 2.0)
                drop['chars'] = [random.choice(self.characters) for _ in range(len(drop['chars']))]
                drop['change_timers'] = [random.randint(5, 20) for _ in range(len(drop['chars']))]
            
            for i in range(len(drop['chars'])):
                drop['change_timers'][i] -= 1
                if drop['change_timers'][i] <= 0:
                    if random.random() < 0.7 / (i + 1):
                        drop['chars'][i] = random.choice(self.characters)
                    drop['change_timers'][i] = random.randint(5, 20)
                
    def draw(self, screen):
        screen.fill((0, 0, 0))
        
        for drop in self.drops:
            y_pos = int(drop['y'])
            for i, char in enumerate(drop['chars']):
                if i < 3:
                    intensity = 255 - (i * 10)
                else:
                    intensity = max(200 - (i * 4), 30)
                
                color = (0, intensity, 0)
                text = self.font.render(char, True, color)
                screen.blit(text, (drop['x'], y_pos - i * self.font_size)) 