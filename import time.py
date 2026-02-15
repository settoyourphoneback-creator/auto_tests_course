import time

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
time.sleep(5)

# Важно: элементы могут не находиться по следующим причинам:
# 1. Сайт ya.ru может редиректить или содержать капчу (проверку на робота), которая появляется при автоматизации.
#    В этом случае Selenium увидит страницу капчи, где нужные элементы отсутствуют.
# 2. Сайт может динамически загружать элементы после загрузки страницы (JavaScript), и time.sleep(5) может быть недостаточно,
#    либо нужные элементы еще не успели появиться.
# 3. Элементы могут появляться только после какого-либо взаимодействия (например, после ввода текста или нажатия).
# 4. Поисковые селекторы могут быть неактуальны: класс или имя поля изменились, элементы были переименованы, скрыты или удалены.
# 5. Сайт может по-разному отображать элементы для разных регионов, браузеров, устройств.
# 6. Иногда Яндекс может полностью скрыть элементы поиска или контент для автоматизации.

# Проверим, попали ли мы на страницу капчи
current_url = driver.current_url
if "captcha" in current_url or "verify" in current_url or "showcaptcha" in current_url:
    print("Мы попали на страницу капчи — Selenium блокируется. Элементы получить нельзя.")
else:
    try:
        # Пробуем получить поле поиска по имени
        search_input = driver.find_element(By.NAME, "text")
        print("Поле поиска найдено")
    except Exception as e:
        print(f"Не удалось найти поле поиска: {e}")

    # Пример проверки других элементов
    try:
        weather_element = driver.find_element(By.CLASS_NAME, "informers3-weather__text")
        print("Элемент погоды найден")
    except Exception as e:
        print(f"Не удалось найти элемент прогноза погоды: {e}")

# Можно также использовать явные ожидания (WebDriverWait), чтобы дождаться появления элементов,
# но если отображается капча — никакие ожидания не помогут, кроме ручного решения капчи.

time.sleep(5)

# Пример класса для поиска кликабельных элементов
class MainPage:
    def __init__(self, driver):
        self.driver = driver

    def clickable_elements(self):
        elements = []
        try:
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            elements.extend(buttons)
            links = self.driver.find_elements(By.TAG_NAME, "a")
            elements.extend(links)
            onclicks = self.driver.find_elements(By.CSS_SELECTOR, "*[onclick]")
            for el in onclicks:
                if el not in elements:
                    elements.append(el)
            input_buttons = self.driver.find_elements(By.CSS_SELECTOR, "input[type='button'], input[type='submit']")
            elements.extend([el for el in input_buttons if el not in elements])
        except Exception as e:
            print(f"Ошибка при поиске кликабельных элементов: {e}")

        # Убираем дубли
        seen = set()
        unique_elements = []
        for el in elements:
            if el not in seen:
                unique_elements.append(el)
                seen.add(el)
        return unique_elements

    def click_all(self):
        elements = self.clickable_elements()
        for el in elements:
            try:
                el.click()
            except Exception as e:
                print(f"Не удалось кликнуть по элементу: {e}")
                print("Найдены кликабельные элементы:")
                for idx, elem in enumerate(elements, 1):
                    try:
                        desc = elem.get_attribute('outerHTML')
                        print(f"{idx}: {desc[:100]}...")
                    except Exception as ex:
                        print(f"{idx}: Не удалось получить HTML элемента: {ex}")
        return elements

# Примечание: если сайт защищён от автоматизации или требует капчу, полноценный сбор элементов невозможен.
# Попробуйте другой сайт или настройте WebDriver для обхода защиты.
