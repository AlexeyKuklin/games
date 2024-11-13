import PyInstaller.__main__
import os

# Убедитесь, что все файлы находятся в одной директории
PyInstaller.__main__.run([
    'chess_game.py',
    '--onefile',
    '--name=ChessGame',
    '--add-data=board.py;.',
    '--add-data=ai.py;.',
    '--console',
]) 