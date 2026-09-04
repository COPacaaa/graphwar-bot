"""
GraphWar Bot - Build EXE версию
Требует: pip install pyinstaller
"""

import os
import sys

def build_exe():
    """Создаёт .exe файл из Python кода"""
    
    print("🔨 Создание EXE файла GraphWar Bot...\n")
    
    # Проверяем, установлен ли PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("❌ PyInstaller не установлен!")
        print("Установи: pip install pyinstaller")
        return False
    
    # Команда для создания EXE
    cmd = 'pyinstaller --onefile --windowed --name "GraphWar Bot" graphwar_bot.py'
    
    print(f"▶️  Выполняем: {cmd}\n")
    result = os.system(cmd)
    
    if result == 0:
        print("\n✅ EXE файл создан!")
        print("📁 Путь: dist/GraphWar Bot.exe")
        return True
    else:
        print("\n❌ Ошибка при создании EXE")
        return False

if __name__ == "__main__":
    build_exe()
