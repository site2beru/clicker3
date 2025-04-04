# 13.03.2025 usp
# чудо-бот для захода на сайты через Яшу (с помощью Дзена) по заданным поисковым запросам
# используем прокси (если нужно), куки и фингерпринты
#
# алгоритм действий следующий:
#
# 1. открываем браузер, заходим на яндекс (через dzen.ru)
# 2. устанавливаем cookie для сайта и заходим снова
# 3. находим iframe с поиском Яндекса, а внутри него поисковую строку
# 4. пишем в строку ключевик и жмем Enter
# 5. ищем нужный нам сайт (задается в конце файла)
# 6. тыкаем на него и сразу сваливаем
# 7. ждем N-ное время и идем еще раз
#
# main — этот файл — исполняет запуск
# proxy_handler — настройки прокси
# browser_config — конфигурация
# website_visitor — процесс поиска по страницам
# user_simulation – настройки девайса пользователя
[#
]# комменты для headless
#
# note: убрать нафиг установку модулей ибо не работает

import random
import time
import logging
import sys
import subprocess
import importlib

# Список необходимых библиотек
REQUIRED_LIBRARIES = {
    'selenium': 'selenium',
    'fake_useragent': 'fake-useragent',
    'requests': 'requests'
}

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_and_install_libraries():
    """Проверяет наличие библиотек и устанавливает их, если они отсутствуют."""
    for module_name, package_name in REQUIRED_LIBRARIES.items():
        try:
            importlib.import_module(module_name)
            logger.info(f"Библиотека '{module_name}' установлена")
        except ImportError:
            logger.warning(f"Библиотека '{module_name}' не найдена, устанавливаем...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
                logger.info(f"Библиотека '{module_name}' успешно установлена")
            except subprocess.CalledProcessError as e:
                logger.error(f"Не удалось установить '{module_name}': {e}")
                sys.exit(1)

# Импорт модулей после проверки
from browser_config import setup_browser
from proxy_handler import get_random_proxy
from user_simulation import get_random_mobile_user_agent, get_random_fingerprint
from website_visitor import WebsiteVisitor

def main():
    check_and_install_libraries()

    visitor = WebsiteVisitor()
    target_region = "Тамбов" # где ищем
    target_website = "laser-tambov.ru" # что ищем
    search_keywords = ["эпиляция тамбов"] # по какому запросу ищем
    max_attempts = 12 # сколько раз ищем
    successful_visits = 0 # щётчег удачных поисков — не изменять

    for attempt in range(max_attempts):
        logger.info(f"Попытка {attempt + 1}/{max_attempts}")

        success = visitor.simulate_visit(target_region, target_website, search_keywords[0], use_proxy=False, max_pages=5)
        if success:
            successful_visits += 1

        else:
            logger.warning("Не удалось найти сайт")
        sleep_time = random.uniform(5, 6) if attempt < 2 else random.uniform(5, 15)
        logger.info(f"Ожидаем {sleep_time:.1f} секунд перед следующей попыткой")
        time.sleep(sleep_time)

    logger.info(f"Успешных заходов — {successful_visits} из {max_attempts}")

if __name__ == "__main__":
    main()