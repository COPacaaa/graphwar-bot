import math
import json
from typing import Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Position:
    """Позиция объекта на плоскости"""
    x: float
    y: float

@dataclass
class GameState:
    """Состояние игры"""
    player_pos: Position
    enemy_pos: Position
    obstacles: list = None
    gravity: float = 9.8
    
    def __post_init__(self):
        if self.obstacles is None:
            self.obstacles = []

class TrajectoryCalculator:
    """Калькулятор траектории выстрелов для Graphwar"""
    
    def __init__(self):
        self.gravity = 9.8
    
    def calculate_linear_shot(self, 
                             player: Position, 
                             enemy: Position,
                             velocity: float = 50) -> Optional[str]:
        """
        Расчёт линейной функции для прямого выстрела
        Формула: y = kx + b
        
        Args:
            player: Позиция игрока
            enemy: Позиция врага
            velocity: Начальная скорость
            
        Returns:
            Строка функции или None
        """
        dx = enemy.x - player.x
        dy = enemy.y - player.y
        
        if dx == 0:
            return None
        
        # Угловой коэффициент (тангенс угла)
        k = dy / dx
        
        # Свободный член (пересечение с осью Y)
        b = player.y - k * player.x
        
        # Формируем уравнение
        if b >= 0:
            return f"y = {k:.4f}*x + {b:.4f}"
        else:
            return f"y = {k:.4f}*x - {abs(b):.4f}"
    
    def calculate_parabolic_shot(self,
                                player: Position,
                                enemy: Position,
                                angle_degrees: Optional[float] = None) -> Optional[str]:
        """
        Расчёт параболической траектории (квадратичная функция)
        Формула: y = ax² + bx + c
        
        Args:
            player: Позиция игрока
            enemy: Позиция врага
            angle_degrees: Угол выстрела (если None, используется оптимальный 45°)
            
        Returns:
            Строка функции или None
        """
        dx = enemy.x - player.x
        dy = enemy.y - player.y
        
        if dx == 0:
            return None
        
        if angle_degrees is None:
            angle_degrees = 45
        
        angle_rad = math.radians(angle_degrees)
        
        # Начальная скорость
        v0 = math.sqrt(self.gravity * dx / (2 * math.cos(angle_rad)**2))
        
        # Коэффициенты параболы
        # y = y0 + x*tan(θ) - (g*x²)/(2*v0²*cos²(θ))
        a = -self.gravity / (2 * v0**2 * math.cos(angle_rad)**2)
        b = math.tan(angle_rad)
        c = player.y
        
        # Проверяем, достигаем ли мы цели
        y_at_enemy = a * (enemy.x - player.x)**2 + b * (enemy.x - player.x) + c
        
        if abs(y_at_enemy - enemy.y) > 1:  # Допуск погрешности
            return None
        
        return f"y = {a:.6f}*(x-{player.x})² + {b:.4f}*(x-{player.x}) + {c:.4f}"
    
    def calculate_optimal_shot(self, game_state: GameState) -> Dict:
        """
        Автоматический расчёт оптимального выстрела
        Пробует разные варианты и выбирает лучший
        
        Args:
            game_state: Состояние игры
            
        Returns:
            Словарь с результатом
        """
        result = {
            "player_pos": (game_state.player_pos.x, game_state.player_pos.y),
            "enemy_pos": (game_state.enemy_pos.x, game_state.enemy_pos.y),
            "shots": []
        }
        
        # Вариант 1: Прямой выстрел
        linear_shot = self.calculate_linear_shot(
            game_state.player_pos,
            game_state.enemy_pos
        )
        if linear_shot:
            result["shots"].append({
                "type": "linear",
                "formula": linear_shot,
                "description": "Прямой выстрел (линейная траектория)"
            })
        
        # Вариант 2: Параболический выстрел при 45°
        parabolic_shot = self.calculate_parabolic_shot(
            game_state.player_pos,
            game_state.enemy_pos,
            angle_degrees=45
        )
        if parabolic_shot:
            result["shots"].append({
                "type": "parabolic_45",
                "formula": parabolic_shot,
                "description": "Параболический выстрел под углом 45°"
            })
        
        # Вариант 3: Параболический выстрел при 30°
        parabolic_shot_30 = self.calculate_parabolic_shot(
            game_state.player_pos,
            game_state.enemy_pos,
            angle_degrees=30
        )
        if parabolic_shot_30:
            result["shots"].append({
                "type": "parabolic_30",
                "formula": parabolic_shot_30,
                "description": "Параболический выстрел под углом 30°"
            })
        
        # Выбираем первый подходящий выстрел
        if result["shots"]:
            result["recommended"] = result["shots"][0]
        
        return result


class GraphwarBot:
    """Главный класс бота Graphwar"""
    
    def __init__(self):
        self.calculator = TrajectoryCalculator()
        self.game_history = []
    
    def aim_and_shoot(self, player_x: float, player_y: float, 
                     enemy_x: float, enemy_y: float) -> Dict:
        """
        Основной метод: целиться и стрелять
        
        Args:
            player_x, player_y: Координаты игрока
            enemy_x, enemy_y: Координаты врага
            
        Returns:
            Рекомендуемая формула для выстрела
        """
        game_state = GameState(
            player_pos=Position(player_x, player_y),
            enemy_pos=Position(enemy_x, enemy_y)
        )
        
        result = self.calculator.calculate_optimal_shot(game_state)
        self.game_history.append(result)
        
        return result
    
    def get_formula(self, player_x: float, player_y: float, 
                   enemy_x: float, enemy_y: float) -> str:
        """
        Получить только формулу для быстрого использования
        
        Returns:
            Строка с формулой
        """
        result = self.aim_and_shoot(player_x, player_y, enemy_x, enemy_y)
        if result.get("recommended"):
            return result["recommended"]["formula"]
        return "Невозможно рассчитать выстрел"
    
    def get_history(self) -> list:
        """Получить историю всех выстрелов"""
        return self.game_history


# Примеры использования
if __name__ == "__main__":
    bot = GraphwarBot()
    
    print("🤖 GraphWar Bot запущен!\n")
    
    # Пример 1: Простой выстрел
    print("=" * 50)
    print("Пример 1: Выстрел в близкую цель")
    print("=" * 50)
    result = bot.aim_and_shoot(
        player_x=0, player_y=0,
        enemy_x=10, enemy_y=5
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 50)
    print("Пример 2: Выстрел в дальнюю цель")
    print("=" * 50)
    result = bot.aim_and_shoot(
        player_x=0, player_y=10,
        enemy_x=50, enemy_y=30
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 50)
    print("Быстрая формула для выстрела:")
    print("=" * 50)
    formula = bot.get_formula(0, 0, 20, 15)
    print(f"📐 Используйте эту формулу: {formula}")
