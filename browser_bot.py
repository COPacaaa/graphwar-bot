"""
Автоматизация GraphWar в браузере с использованием Selenium
Требует: pip install selenium
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from graphwar_bot import GraphwarBot

class GraphwarBrowserBot:
    """Автоматический бот для игры в GraphWar через браузер"""
    
    def __init__(self, headless=False):
        """
        Инициализация браузера
        
        Args:
            headless: Если True, браузер работает в фоне без окна
        """
        self.bot = GraphwarBot()
        
        # Настройки Chrome
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Запускаем браузер
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def open_game(self):
        """Открыть игру на graphwar.com"""
        print("🌐 Открываем GraphWar...")
        self.driver.get("https://graphwar.com/")
        time.sleep(2)
        print("✅ Игра загружена!")
    
    def find_input_field(self):
        """Найти поле ввода формулы"""
        try:
            # Пытаемся найти поле ввода разными селекторами
            selectors = [
                (By.ID, "formula"),
                (By.ID, "function"),
                (By.NAME, "formula"),
                (By.CLASS_NAME, "formula-input"),
                (By.XPATH, "//input[@type='text']"),
                (By.XPATH, "//textarea"),
            ]
            
            for by, selector in selectors:
                try:
                    element = self.driver.find_element(by, selector)
                    if element.is_displayed():
                        return element
                except:
                    continue
            
            print("⚠️  Не удалось найти поле ввода")
            return None
        except Exception as e:
            print(f"❌ Ошибка при поиске поля: {e}")
            return None
    
    def find_shoot_button(self):
        """Найти кнопку для выстрела"""
        try:
            buttons = [
                (By.ID, "shoot"),
                (By.ID, "fire"),
                (By.ID, "shoot-button"),
                (By.CLASS_NAME, "shoot-btn"),
                (By.XPATH, "//button[contains(text(), 'Shoot')]"),
                (By.XPATH, "//button[contains(text(), 'Fire')]"),
                (By.XPATH, "//button[contains(text(), 'Стрелять')]"),
                (By.XPATH, "//button[contains(text(), 'Выстрелить')]"),
            ]
            
            for by, selector in buttons:
                try:
                    element = self.driver.find_element(by, selector)
                    if element.is_displayed():
                        return element
                except:
                    continue
            
            print("⚠️  Не удалось найти кнопку выстрела")
            return None
        except Exception as e:
            print(f"❌ Ошибка при поиске кнопки: {e}")
            return None
    
    def shoot(self, formula):
        """
        Выстрелить с заданной формулой
        
        Args:
            formula: Строка с математической формулой (например "y = 0.5*x")
        """
        try:
            # Находим поле ввода
            input_field = self.find_input_field()
            if not input_field:
                print("❌ Не найдено поле ввода")
                return False
            
            # Очищаем поле
            input_field.clear()
            time.sleep(0.5)
            
            # Вводим формулу
            print(f"📝 Вводим формулу: {formula}")
            input_field.send_keys(formula)
            time.sleep(0.5)
            
            # Находим кнопку выстрела
            shoot_btn = self.find_shoot_button()
            if not shoot_btn:
                print("❌ Не найдена кнопка выстрела")
                return False
            
            # Нажимаем кнопку
            print("💥 ВЫСТРЕЛИЛИ!")
            shoot_btn.click()
            time.sleep(1)
            
            return True
        except Exception as e:
            print(f"❌ Ошибка при выстреле: {e}")
            return False
    
    def auto_shoot_to_enemy(self, player_x, player_y, enemy_x, enemy_y):
        """
        Автоматически рассчитать и выстрелить в врага
        
        Args:
            player_x, player_y: Координаты игрока
            enemy_x, enemy_y: Координаты врага
        """
        # Рассчитываем формулу
        formula = self.bot.get_formula(player_x, player_y, enemy_x, enemy_y)
        print(f"\n🎯 Цель: ({enemy_x}, {enemy_y})")
        print(f"📐 Рассчитанная формула: {formula}")
        
        # Выстреливаем
        return self.shoot(formula)
    
    def take_screenshot(self, filename="screenshot.png"):
        """Сделать скриншот"""
        self.driver.save_screenshot(filename)
        print(f"📸 Скриншот сохранён: {filename}")
    
    def close(self):
        """Закрыть браузер"""
        self.driver.quit()
        print("🔌 Браузер закрыт")
    
    def get_page_source(self):
        """Получить исходный код страницы"""
        return self.driver.page_source
    
    def print_page_elements(self):
        """Вывести все элементы для дебага"""
        print("\n📋 Все текстовые поля на странице:")
        inputs = self.driver.find_elements(By.TAG_NAME, "input")
        for i, inp in enumerate(inputs):
            print(f"  [{i}] {inp.get_attribute('id')} | {inp.get_attribute('name')} | {inp.get_attribute('class')}")
        
        print("\n📋 Все кнопки на странице:")
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        for i, btn in enumerate(buttons):
            print(f"  [{i}] {btn.text} | {btn.get_attribute('id')} | {btn.get_attribute('class')}")


def main():
    """Пример использования браузерного бота"""
    
    print("🤖 GraphWar Browser Bot")
    print("="*50)
    
    # Создаём бота (headless=True для фонового режима)
    bot = GraphwarBrowserBot(headless=False)
    
    try:
        # Открываем игру
        bot.open_game()
        
        # Выводим элементы на странице для дебага
        print("\n🔍 Сканирование страницы...\n")
        bot.print_page_elements()
        
        # Даём время пользователю разобраться
        print("\n⏳ Ожидание 5 секунд перед выстрелом...")
        time.sleep(5)
        
        # Примеры выстрелов
        print("\n" + "="*50)
        print("🎯 АВТОМАТИЧЕСКИЕ ВЫСТРЕЛЫ")
        print("="*50)
        
        # Выстрел 1
        bot.auto_shoot_to_enemy(0, 0, 50, 30)
        time.sleep(2)
        
        # Выстрел 2
        bot.auto_shoot_to_enemy(0, 0, 100, 50)
        time.sleep(2)
        
        # Выстрел 3
        bot.auto_shoot_to_enemy(10, 10, 60, 40)
        time.sleep(2)
        
        print("\n✅ Все выстрелы выполнены!")
        
        # Сохраняем скриншот
        bot.take_screenshot()
        
        # Ждём перед закрытием
        print("\n⏳ Браузер закроется через 5 секунд...")
        time.sleep(5)
        
    finally:
        # Закрываем браузер
        bot.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⛔ Прервано пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
