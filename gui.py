"""
GraphWar Bot - GUI версия с Tkinter
Графический интерфейс для расчёта выстрелов
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
from graphwar_bot import GraphwarBot

class GraphwarBotGUI:
    """Графический интерфейс для GraphWar Bot"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 GraphWar Bot")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Иконка окна
        self.root.configure(bg="#1e1e1e")
        
        # Инициализируем бота
        self.bot = GraphwarBot()
        
        # Создаём интерфейс
        self.create_widgets()
    
    def create_widgets(self):
        """Создаёт все элементы интерфейса"""
        
        # Заголовок
        title_frame = ttk.Frame(self.root)
        title_frame.pack(pady=20, padx=20, fill=tk.X)
        
        title_label = ttk.Label(
            title_frame,
            text="🎯 GraphWar Bot - Калькулятор траекторий",
            font=("Arial", 16, "bold")
        )
        title_label.pack()
        
        # Основная рамка
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # ===== ПОЗИЦИЯ ИГРОКА =====
        player_label = ttk.LabelFrame(main_frame, text="📌 Ваша позиция", padding=10)
        player_label.pack(fill=tk.X, pady=10)
        
        # Игрок X
        ttk.Label(player_label, text="X координата:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.player_x = ttk.Entry(player_label, width=15)
        self.player_x.insert(0, "0")
        self.player_x.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Игрок Y
        ttk.Label(player_label, text="Y координата:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.player_y = ttk.Entry(player_label, width=15)
        self.player_y.insert(0, "0")
        self.player_y.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        # ===== ПОЗИЦИЯ ВРАГА =====
        enemy_label = ttk.LabelFrame(main_frame, text="🎯 Позиция врага", padding=10)
        enemy_label.pack(fill=tk.X, pady=10)
        
        # Враг X
        ttk.Label(enemy_label, text="X координата:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.enemy_x = ttk.Entry(enemy_label, width=15)
        self.enemy_x.insert(0, "50")
        self.enemy_x.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Враг Y
        ttk.Label(enemy_label, text="Y координата:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.enemy_y = ttk.Entry(enemy_label, width=15)
        self.enemy_y.insert(0, "30")
        self.enemy_y.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        # ===== КНОПКИ =====
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=15)
        
        # Кнопка "Рассчитать"
        calc_btn = ttk.Button(
            button_frame,
            text="🎯 Рассчитать выстрел",
            command=self.calculate
        )
        calc_btn.pack(side=tk.LEFT, padx=5)
        
        # Кнопка "Очистить"
        clear_btn = ttk.Button(
            button_frame,
            text="🔄 Очистить",
            command=self.clear
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # ===== РЕЗУЛЬТАТ =====
        result_label = ttk.LabelFrame(main_frame, text="📐 Результат", padding=10)
        result_label.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Текстовое поле для результата
        self.result_text = tk.Text(result_label, height=15, width=70, font=("Courier", 10))
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(self.result_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.result_text.yview)
        
        # ===== КНОПКИ КОПИРОВАНИЯ =====
        copy_frame = ttk.Frame(main_frame)
        copy_frame.pack(fill=tk.X, pady=10)
        
        copy_btn = ttk.Button(
            copy_frame,
            text="📋 Копировать формулу",
            command=self.copy_formula
        )
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        export_btn = ttk.Button(
            copy_frame,
            text="💾 Сохранить как JSON",
            command=self.export_json
        )
        export_btn.pack(side=tk.LEFT, padx=5)
    
    def calculate(self):
        """Рассчитать траекторию"""
        try:
            # Получаем координаты
            player_x = float(self.player_x.get())
            player_y = float(self.player_y.get())
            enemy_x = float(self.enemy_x.get())
            enemy_y = float(self.enemy_y.get())
            
            # Рассчитываем
            result = self.bot.aim_and_shoot(player_x, player_y, enemy_x, enemy_y)
            
            # Очищаем поле результата
            self.result_text.delete(1.0, tk.END)
            
            # Выводим результат
            output = f"✅ РАСЧЁТ ВЫПОЛНЕН\n"
            output += "="*60 + "\n\n"
            
            output += f"📍 Позиция игрока: ({player_x}, {player_y})\n"
            output += f"🎯 Позиция врага: ({enemy_x}, {enemy_y})\n"
            
            # Расстояние
            distance = ((enemy_x - player_x)**2 + (enemy_y - player_y)**2)**0.5
            output += f"📏 Расстояние: {distance:.2f}\n\n"
            
            output += "="*60 + "\n"
            output += "💡 ДОСТУПНЫЕ ВАРИАНТЫ ВЫСТРЕЛОВ:\n"
            output += "="*60 + "\n\n"
            
            for i, shot in enumerate(result['shots'], 1):
                output += f"Вариант #{i}: {shot['type'].upper()}\n"
                output += f"  Описание: {shot['description']}\n"
                output += f"  📐 Формула: {shot['formula']}\n\n"
            
            output += "="*60 + "\n"
            output += "🎯 РЕКОМЕНДУЕТСЯ:\n"
            output += "="*60 + "\n"
            if result.get('recommended'):
                rec = result['recommended']
                output += f"Тип: {rec['type']}\n"
                output += f"Описание: {rec['description']}\n"
                output += f"📐 Формула:\n\n"
                output += f"   {rec['formula']}\n\n"
                output += "✅ Используйте эту формулу в игре!\n"
            
            self.result_text.insert(tk.END, output)
            
            # Сохраняем последний результат
            self.last_result = result
            
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числовые значения!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
    
    def clear(self):
        """Очистить все поля"""
        self.player_x.delete(0, tk.END)
        self.player_x.insert(0, "0")
        self.player_y.delete(0, tk.END)
        self.player_y.insert(0, "0")
        self.enemy_x.delete(0, tk.END)
        self.enemy_x.insert(0, "50")
        self.enemy_y.delete(0, tk.END)
        self.enemy_y.insert(0, "30")
        self.result_text.delete(1.0, tk.END)
    
    def copy_formula(self):
        """Копировать формулу в буфер обмена"""
        try:
            if hasattr(self, 'last_result') and self.last_result.get('recommended'):
                formula = self.last_result['recommended']['formula']
                self.root.clipboard_clear()
                self.root.clipboard_append(formula)
                messagebox.showinfo("✅ Успех", f"Формула скопирована:\n\n{formula}")
            else:
                messagebox.showwarning("⚠️  Внимание", "Сначала рассчитайте выстрел!")
        except Exception as e:
            messagebox.showerror("❌ Ошибка", str(e))
    
    def export_json(self):
        """Экспортировать результат в JSON"""
        try:
            if hasattr(self, 'last_result'):
                filename = "graphwar_result.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.last_result, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("✅ Успех", f"Результат сохранён в {filename}")
            else:
                messagebox.showwarning("⚠️  Внимание", "Сначала рассчитайте выстрел!")
        except Exception as e:
            messagebox.showerror("❌ Ошибка", str(e))


def main():
    """Запуск приложения"""
    root = tk.Tk()
    app = GraphwarBotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
