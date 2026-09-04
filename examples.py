"""
Примеры использования GraphWar Bot
"""

from graphwar_bot import GraphwarBot, GameState, Position
import json

def example_1_simple_shot():
    """Пример 1: Простой выстрел в близкую цель"""
    print("\n" + "="*60)
    print("📍 ПРИМЕР 1: Простой выстрел в близкую цель")
    print("="*60)
    
    bot = GraphwarBot()
    
    # Ваши координаты: (0, 0)
    # Враг находится на: (10, 5)
    result = bot.aim_and_shoot(0, 0, 10, 5)
    
    print(f"📌 Ваша позиция: {result['player_pos']}")
    print(f"🎯 Позиция врага: {result['enemy_pos']}")
    print(f"\n💡 Рекомендуемая формула:")
    print(f"   {result['recommended']['formula']}")
    print(f"   Тип: {result['recommended']['type']}")
    

def example_2_multiple_shots():
    """Пример 2: Несколько врагов - несколько выстрелов"""
    print("\n" + "="*60)
    print("🎮 ПРИМЕР 2: Несколько врагов")
    print("="*60)
    
    bot = GraphwarBot()
    your_pos = (0, 0)
    
    enemies = [
        ("Враг 1", 10, 5),
        ("Враг 2", 20, 15),
        ("Враг 3", 50, 30),
        ("Враг 4", 100, 50),
    ]
    
    for name, x, y in enemies:
        formula = bot.get_formula(your_pos[0], your_pos[1], x, y)
        print(f"\n{name} на позиции ({x}, {y}):")
        print(f"   Формула: {formula}")


def example_3_all_variants():
    """Пример 3: Все варианты выстрелов"""
    print("\n" + "="*60)
    print("🔄 ПРИМЕР 3: Все варианты траекторий")
    print("="*60)
    
    bot = GraphwarBot()
    result = bot.aim_and_shoot(0, 10, 50, 30)
    
    print(f"📌 От позиции {result['player_pos']} до {result['enemy_pos']}")
    print(f"\n💎 Все возможные варианты выстрелов:\n")
    
    for i, shot in enumerate(result['shots'], 1):
        print(f"{i}. {shot['description']}")
        print(f"   Тип: {shot['type']}")
        print(f"   Формула: {shot['formula']}")
        print()


def example_4_game_session():
    """Пример 4: Имитация боевой сессии"""
    print("\n" + "="*60)
    print("⚔️  ПРИМЕР 4: Боевая сессия (5 выстрелов)")
    print("="*60)
    
    bot = GraphwarBot()
    your_pos = (0, 0)
    
    # Враги приближаются к вам
    enemies_positions = [
        (15, 8),
        (25, 20),
        (40, 35),
        (60, 45),
        (80, 55),
    ]
    
    print(f"\n🛡️  Вы находитесь на позиции {your_pos}")
    print("🔴 Враги приближаются!\n")
    
    for shot_num, (x, y) in enumerate(enemies_positions, 1):
        distance = (x**2 + y**2)**0.5
        formula = bot.get_formula(your_pos[0], your_pos[1], x, y)
        
        print(f"Выстрел #{shot_num}")
        print(f"  Враг на: ({x}, {y})")
        print(f"  Расстояние: {distance:.1f}")
        print(f"  Формула: {formula}")
        print(f"  ✅ БАБАХ! Враг уничтожен!\n")


def example_5_json_export():
    """Пример 5: Экспорт результатов в JSON"""
    print("\n" + "="*60)
    print("💾 ПРИМЕР 5: Экспорт результатов")
    print("="*60)
    
    bot = GraphwarBot()
    
    # Делаем несколько выстрелов
    bot.aim_and_shoot(0, 0, 10, 5)
    bot.aim_and_shoot(0, 0, 50, 30)
    bot.aim_and_shoot(10, 10, 60, 40)
    
    # Получаем историю
    history = bot.get_history()
    
    # Выводим в красивом JSON формате
    json_data = {
        "total_shots": len(history),
        "shots": [
            {
                "from": shot["player_pos"],
                "to": shot["enemy_pos"],
                "formula": shot["recommended"]["formula"] if shot.get("recommended") else "N/A"
            }
            for shot in history
        ]
    }
    
    print("\n📋 История боевых действий:\n")
    print(json.dumps(json_data, indent=2))
    
    # Сохраняем в файл
    with open("battle_history.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    print("\n✅ История сохранена в battle_history.json")


def example_6_interactive():
    """Пример 6: Интерактивный режим"""
    print("\n" + "="*60)
    print("🎯 ПРИМЕР 6: Интерактивный режим")
    print("="*60)
    
    bot = GraphwarBot()
    
    print("\n🕹️  Интерактивный калькулятор траекторий\n")
    
    # Примеры координат
    test_cases = [
        {"name": "Враг справа", "player": (0, 0), "enemy": (20, 10)},
        {"name": "Враг выше", "player": (0, 0), "enemy": (10, 20)},
        {"name": "Враг диагонально вверх-вправо", "player": (5, 5), "enemy": (25, 30)},
        {"name": "Враг далеко", "player": (0, 0), "enemy": (100, 50)},
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n[{i}] {case['name']}")
        print(f"    От: {case['player']} → До: {case['enemy']}")
        
        formula = bot.get_formula(
            case['player'][0], case['player'][1],
            case['enemy'][0], case['enemy'][1]
        )
        print(f"    📐 Формула: {formula}")


def example_7_performance():
    """Пример 7: Тест производительности"""
    print("\n" + "="*60)
    print("⚡ ПРИМЕР 7: Тест производительности")
    print("="*60)
    
    import time
    
    bot = GraphwarBot()
    
    print("\n🔄 Расчёт 100 выстрелов...\n")
    
    start_time = time.time()
    
    # Генерируем случайные позиции
    for i in range(100):
        x = (i * 7) % 200  # Квазислучайные координаты
        y = (i * 13) % 150
        bot.get_formula(0, 0, x, y)
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    print(f"✅ Готово!")
    print(f"⏱️  Время: {elapsed:.3f} сек")
    print(f"📊 Среднее время на выстрел: {(elapsed/100)*1000:.2f} мс")
    print(f"🚀 Пропускная способность: {100/elapsed:.0f} выстр/сек")


def example_8_visualization():
    """Пример 8: Визуализация траектории в текста"""
    print("\n" + "="*60)
    print("📊 ПРИМЕР 8: Визуализация траектории")
    print("="*60)
    
    def draw_trajectory(player_x, player_y, enemy_x, enemy_y):
        """Простая текстовая визуализация"""
        
        print(f"\n📍 Позиция игрока: ({player_x}, {player_y})")
        print(f"🎯 Позиция врага: ({enemy_x}, {enemy_y})\n")
        
        # Создаём сетку
        width = max(20, enemy_x + 5)
        height = max(10, max(player_y, enemy_y) + 5)
        
        grid = [['·' for _ in range(width)] for _ in range(height)]
        
        # Рисуем позиции
        if 0 <= player_y < height and 0 <= player_x < width:
            grid[int(player_y)][int(player_x)] = 'P'
        if 0 <= enemy_y < height and 0 <= enemy_x < width:
            grid[int(enemy_y)][int(enemy_x)] = 'E'
        
        # Выводим сетку
        for row in reversed(grid):
            print(''.join(row))
        
        # Легенда
        print("\nЛегенда: P = Player (Игрок), E = Enemy (Враг), · = Пусто")
    
    # Рисуем несколько траекторий
    scenarios = [
        (0, 0, 15, 8),
        (0, 5, 20, 15),
        (5, 5, 25, 20),
    ]
    
    for player_x, player_y, enemy_x, enemy_y in scenarios:
        draw_trajectory(player_x, player_y, enemy_x, enemy_y)


def main():
    """Главная функция - запускает все примеры"""
    
    print("\n" + "🤖 "*20)
    print("ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ GraphWar Bot")
    print("🤖 "*20)
    
    # Раскомментируйте нужные примеры:
    
    example_1_simple_shot()           # Простой выстрел
    example_2_multiple_shots()         # Несколько врагов
    example_3_all_variants()          # Все варианты
    example_4_game_session()          # Боевая сессия
    example_5_json_export()           # Экспорт JSON
    example_6_interactive()           # Интерактивный режим
    example_7_performance()           # Тест производительности
    example_8_visualization()         # Визуализация
    
    print("\n" + "="*60)
    print("✅ ВСЕ ПРИМЕРЫ ВЫПОЛНЕНЫ!")
    print("="*60)
    print("\n📚 Документация: см. USAGE.md")
    print("💻 Основной модуль: graphwar_bot.py")
    print("🌐 GitHub: https://github.com/COPacaaa/graphwar-bot\n")


if __name__ == "__main__":
    main()
