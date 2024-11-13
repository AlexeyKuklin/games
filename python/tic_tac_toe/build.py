import PyInstaller.__main__
import os
import glob

# Получаем абсолютный путь к текущей директории
current_dir = os.path.dirname(os.path.abspath(__file__))

# Проверяем наличие файлов
sound_dir = os.path.join(current_dir, 'sound')
font_dir = os.path.join(current_dir, 'font')
font_file = os.path.join(font_dir, 'msmincho.ttc')
icon_file = os.path.join(current_dir, 'icon.ico')

if not os.path.exists(sound_dir):
    print(f"Папка со звуками не найдена: {sound_dir}")
    exit(1)

if not os.path.exists(font_file):
    print(f"Файл шрифта не найден: {font_file}")
    exit(1)

# Получаем список звуковых файлов
sound_files = []
for wav_file in glob.glob(os.path.join(sound_dir, '*.wav')):
    sound_files.append(f'--add-data={wav_file};sound')

# Формируем параметры для PyInstaller
params = [
    'main.py',
    '--onefile',
    '--windowed',
    '--name=Matrix TicTacToe',
    '--clean',
    '--distpath=build',
    '--workpath=build/temp',
    '--specpath=build',
    # Добавляем каждый звуковой файл отдельно
    *sound_files,
    # Добавляем шрифт
    f'--add-data={font_file};font',
    # Исключаем ненужные модули
    '--exclude-module=tkinter',
    '--exclude-module=turtle',
    '--exclude-module=numpy',
    '--exclude-module=PIL',
    '--exclude-module=cv2'
]

# Добавляем иконку если она существует
if os.path.exists(icon_file):
    params.append(f'--icon={icon_file}')

print("Сборка с параметрами:", params)
print("Текущая директория:", current_dir)
print("Путь к звукам:", sound_dir)
print("Путь к шрифту:", font_file)
print("Найденные звуковые файлы:", sound_files)

# Запускаем PyInstaller
PyInstaller.__main__.run(params) 