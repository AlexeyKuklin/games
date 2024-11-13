import numpy as np
from scipy.io import wavfile
from scipy import signal
import os

class MatrixSoundGenerator:
    def __init__(self):
        self.sample_rate = 44100
        self.sound_dir = 'sound'
        
        # Создаем директорию для звуков, если её нет
        if not os.path.exists(self.sound_dir):
            os.makedirs(self.sound_dir)
    
    def _normalize_waveform(self, waveform):
        """Нормализация волны для предотвращения искажений"""
        return (waveform * 32767 / np.max(np.abs(waveform))).astype(np.int16)
    
    def generate_move_sound(self):
        """Более мягкий цифровой клик"""
        duration = 0.08
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        frequency = 1500
        waveform = (signal.square(2 * np.pi * frequency * t) * 0.2 + 
                   np.sin(2 * np.pi * frequency * t) * 0.8) * np.exp(-20 * t)
        
        waveform = self._normalize_waveform(waveform)
        wavfile.write(os.path.join(self.sound_dir, 'move.wav'), self.sample_rate, waveform)
    
    def generate_win_sound(self):
        """Более плавная восходящая последовательность"""
        duration = 0.6
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        frequencies = [440, 660, 880, 1100]
        waveform = np.zeros_like(t)
        
        for i, f in enumerate(frequencies):
            wave = (signal.square(2 * np.pi * f * t) * 0.1 + 
                   np.sin(2 * np.pi * f * t) * 0.9) * np.exp(-5 * (t - i * duration/len(frequencies)))
            waveform += wave
        
        waveform = self._normalize_waveform(waveform)
        wavfile.write(os.path.join(self.sound_dir, 'win.wav'), self.sample_rate, waveform)
    
    def generate_lose_sound(self):
        """Более плавная нисходящая последовательность"""
        duration = 0.6
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        frequencies = [1100, 880, 660, 440]
        waveform = np.zeros_like(t)
        
        for i, f in enumerate(frequencies):
            wave = (signal.square(2 * np.pi * f * t) * 0.15 + 
                   signal.sawtooth(2 * np.pi * f * t) * 0.15 +
                   np.sin(2 * np.pi * f * t) * 0.7) * np.exp(-5 * (t - i * duration/len(frequencies)))
            waveform += wave
        
        waveform = self._normalize_waveform(waveform)
        wavfile.write(os.path.join(self.sound_dir, 'lose.wav'), self.sample_rate, waveform)
    
    def generate_draw_sound(self):
        """Более мягкий нейтральный звук"""
        duration = 0.4
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        frequency = 660
        waveform = (signal.square(2 * np.pi * frequency * t) * 0.1 +
                   signal.sawtooth(2 * np.pi * frequency * 1.5 * t) * 0.1 +
                   np.sin(2 * np.pi * frequency * t) * 0.8) * np.exp(-8 * t)
        
        waveform = self._normalize_waveform(waveform)
        wavfile.write(os.path.join(self.sound_dir, 'draw.wav'), self.sample_rate, waveform)
    
    def generate_background_sound(self):
        """Генерация мягкого фонового эмбиента в стиле матрицы"""
        duration = 10.0
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # Основной низкочастотный гул (более мягкий)
        base_freq = 40  # Снизили частоту
        base_wave = (np.sin(2 * np.pi * base_freq * t) * 0.2 + 
                    np.sin(2 * np.pi * (base_freq * 1.5) * t) * 0.1) # Добавили гармонику
        
        # Медленно меняющиеся гармоники
        harmonic_waves = np.zeros_like(t)
        frequencies = [220, 330, 440]  # Более низкие частоты
        for freq in frequencies:
            phase = np.random.random() * 2 * np.pi
            # Медленная модуляция амплитуды
            amp_mod = 0.5 + 0.5 * np.sin(2 * np.pi * 0.1 * t + phase)
            harmonic_waves += (np.sin(2 * np.pi * freq * t + phase) * 
                             0.05 * amp_mod)  # Уменьшили амплитуду
        
        # "Цифровой дождь" - более редкие и мягкие капли
        drips = np.zeros_like(t)
        for _ in range(10):  # Уменьшили количество капель
            start_time = np.random.random() * (duration - 0.2)
            drip_t = np.maximum(0, t - start_time)
            freq = 1000 + np.random.random() * 500  # Снизили частоту
            drips += (np.sin(2 * np.pi * freq * drip_t) * 
                     np.exp(-30 * drip_t) * 0.05)  # Сделали мягче затухание
        
        # Медленная пульсация
        pulse = 0.8 + 0.2 * np.sin(2 * np.pi * 0.2 * t)
        
        # Комбинируем все элементы с плавными переходами
        waveform = (base_wave + harmonic_waves + drips) * pulse
        
        # Добавляем плавное нарастание и затухание в начале и конце
        fade_duration = 0.5  # секунды
        fade_samples = int(fade_duration * self.sample_rate)
        fade_in = np.linspace(0, 1, fade_samples)
        fade_out = np.linspace(1, 0, fade_samples)
        
        waveform[:fade_samples] *= fade_in
        waveform[-fade_samples:] *= fade_out
        
        # Применяем мягкий фильтр для сглаживания
        from scipy.signal import savgol_filter
        waveform = savgol_filter(waveform, 101, 2)
        
        # Нормализуем и сохраняем
        waveform = self._normalize_waveform(waveform)
        wavfile.write(os.path.join(self.sound_dir, 'background.wav'), 
                     self.sample_rate, waveform)
    
    def generate_click_sound(self):
        """Генерация короткого цифрового клика в стиле матрицы"""
        duration = 0.05  # Очень короткий звук
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # Основная частота и гармоники
        frequency = 2000
        waveform = (
            np.sin(2 * np.pi * frequency * t) * 0.6 +  # Основной тон
            np.sin(2 * np.pi * frequency * 1.5 * t) * 0.2 +  # Верхняя гармоника
            signal.square(2 * np.pi * frequency * 0.5 * t) * 0.2  # Нижняя частота для "цифрового" звучания
        )
        
        # Быстрое затухание для четкого клика
        envelope = np.exp(-50 * t)
        waveform = waveform * envelope
        
        waveform = self._normalize_waveform(waveform)
        wavfile.write(os.path.join(self.sound_dir, 'click.wav'), self.sample_rate, waveform)
    
    def generate_all_sounds(self):
        """Генерация всех звуковых эффектов"""
        self.generate_move_sound()
        self.generate_win_sound()
        self.generate_lose_sound()
        self.generate_draw_sound()
        self.generate_background_sound()
        self.generate_click_sound()  # Добавляем генерацию нового звука
        print("Звуковые файлы в стиле Матрицы созданы в папке sound/")

if __name__ == "__main__":
    generator = MatrixSoundGenerator()
    generator.generate_all_sounds()