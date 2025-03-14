import random
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, InvalidCookieDomainException
from browser_config import setup_browser
from proxy_handler import get_random_proxy
from user_simulation import get_random_mobile_user_agent, get_random_fingerprint

logger = logging.getLogger(__name__)

# посещение dzen, яндекс и сайта

import random
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from browser_config import setup_browser
from proxy_handler import get_random_proxy
from user_simulation import get_random_mobile_user_agent, get_random_fingerprint

logger = logging.getLogger(__name__)

class WebsiteVisitor:
    def __init__(self):
        self.search_url = 'https://dzen.ru'
        self.result_selectors = [
            '.serp-item a.link',               # Мобильная версия
            '.serp-item a.Link_theme_normal',  # Мобильная версия
            '.organic__url',                   # Мобильная версия
            '//a[contains(@href, "clck.yandex.ru")]',  # Мобильная версия
            '//a[contains(@class, "OrganicTitle-Link")]',  # Десктопная версия
            '//a[contains(@class, "link_theme_outer")]',   # Десктопная версия
            '//h3[contains(@class, "OrganicTitle")]/parent::a'  # Десктопная версия
        ]
        self.next_page_selectors = [
            '.Pager',                          # Мобильная версия
            '.Pager-Item',                     # Мобильная версия
            '//a[contains(@class, "pager__item") and contains(@href, "page=")]',  # Мобильная версия
            '//a[contains(@class, "Pager-Item") and contains(text(), "Вперед")]',  # Десктопная версия
            '//a[contains(@class, "Pager-Item_type_next")]'  # Десктопная версия
        ]

    def simulate_visit(self, target_website, search_query, use_proxy=True, max_pages=5):
        attempt = 0
        max_attempts = 100

        if isinstance(search_query, list):
            search_query = search_query[0]
            logger.info(f"Запрос: {search_query}")

        while attempt < max_attempts:
            attempt += 1
            logger.info(f"Попытка {attempt} в этой итерации")

            user_agent = get_random_mobile_user_agent()
            fingerprint = get_random_fingerprint()
            proxy = get_random_proxy() if use_proxy else None

            driver = None
            try:
                driver = setup_browser(user_agent, fingerprint, proxy, headless=False, initial_url=self.search_url)

                logger.info(f"Загружаем {self.search_url}")
                driver.get(self.search_url)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                try:
                    driver.add_cookie({"name": "session_id", "value": f"session_{random.randint(1000, 9999)}", "domain": "dzen.ru"})
                    logger.info("Установлен cookie для домена: dzen.ru")
                except InvalidCookieDomainException:
                    logger.warning("Не удалось установить cookie, продолжаем без него")

                logger.info("Открываем dzen.ru")

                if self._check_captcha(driver):
                    logger.warning("Нашли капчу на начальной странице dzen.ru, продолжаем")

                try:
                    search_input = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//input[@aria-label="Запрос"]'))
                    )
                    logger.info("Поисковая строка найдена напрямую на странице")
                except TimeoutException:
                    logger.info("Поисковая строка не найдена напрямую, ищем в iframe")
                    try:
                        iframe = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, '//iframe[contains(@src, "dzen.ru")]'))
                        )
                        driver.switch_to.frame(iframe)
                        search_input = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//input[@aria-label="Запрос"]'))
                        )
                        logger.info("Поисковая строка найдена в iframe")
                    except TimeoutException:
                        logger.error("Не удалось найти поисковую строку ни напрямую, ни в iframe")
                        driver.save_screenshot(f"search_input_error_{int(time.time())}.png")
                        driver.quit()
                        return False

                search_input.click()
                logger.info(f"Вводим запрос: {search_query}")
                search_input.send_keys(search_query)
                search_input.send_keys(Keys.ENTER)
                logger.info("Нажали Enter")
                driver.switch_to.default_content()

                # Проверяем, куда нас перенаправило
                try:
                    WebDriverWait(driver, 5).until(
                        lambda d: "yandex" in d.current_url or len(d.window_handles) > 1
                    )
                    if len(driver.window_handles) > 1:
                        driver.switch_to.window(driver.window_handles[-1])
                        logger.info(f"Переключились на {driver.current_url}")
                except TimeoutException:
                    logger.info(f"Остались на: {driver.current_url}")

                # Проверяем капчу на Яндексе и перезапускаем с новым браузером
                if "yandex" in driver.current_url and self._check_captcha(driver):
                    logger.warning("Обнаружена капча на странице Яндекса, перезапуск")
                    driver.quit()
                    continue

                # Ожидаем загрузки результатов поиска
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'serp-item')] | //li[contains(@class, 'serp-item')]"))
                    )
                    logger.info("Результаты поиска загружены")
                except TimeoutException:
                    logger.error(f"Не удалось найти результаты поиска. URL: {driver.current_url}")
                    driver.save_screenshot(f"search_results_error_{int(time.time())}.png")
                    driver.quit()
                    continue

                # Ищем и кликаем на целевой сайт
                for page in range(max_pages):
                    logger.info(f"Ищем на странице {page + 1}/{max_pages}")
                    found = self._find_and_click_target(driver, target_website)
                    if found:
                        visit_time = random.uniform(0.1, 0.3)
                        logger.info(f"Зашли и вышли Морти, приключение на {visit_time:.1f} секунд!")
                        time.sleep(visit_time)
                        logger.info("Успешно сходили на сайт")
                        driver.quit()
                        return True

                    if page < max_pages - 1 and self._go_to_next_page(driver):
                        time.sleep(random.uniform(1.0, 3.0))
                    else:
                        logger.info("Дальше страниц нет или переход не удался")
                        break

                logger.warning(f"Не нашли {target_website} в пределах {max_pages} страниц")
                driver.quit()
                continue

            except Exception as e:
                logger.error(f"Ошибка: {e}", exc_info=True)
                if driver:
                    driver.save_screenshot(f"error_{int(time.time())}.png")
                    driver.quit()
                return False

        logger.error(f"Достигнуто максимальное количество попыток ({max_attempts})")
        return False

    def _check_captcha(self, driver):
        captcha_indicators = [
            '//input[@name="rep"]',
            '//img[contains(@src, "captcha")]',
            '//*[contains(text(), "Подтвердите, что вы не робот")]'
        ]
        return any(driver.find_elements(By.XPATH, indicator) for indicator in captcha_indicators)

    def _find_and_click_target(self, driver, target_website):
        intercept_script = """
            window.open = function(url) {
                var win = window.open('');
                win.close();
                return null;
            };
        """
        driver.execute_script(intercept_script)

        for selector in self.result_selectors:
            try:
                method = By.XPATH if selector.startswith('//') else By.CSS_SELECTOR
                results = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((method, selector)))
                for result in results:
                    href = result.get_attribute('href')
                    if href:
                        logger.debug(f"Нашли ссылку {href}")
                        if target_website in href:
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", result)
                            logger.info(f"Кликаем на {href} и уходим")
                            try:
                                driver.execute_script("arguments[0].click();", result)
                                if len(driver.window_handles) > 1:
                                    driver.switch_to.window(driver.window_handles[-1])
                                    logger.warning("Закрыли вкладку с сайтом")
                                    driver.close()
                                    driver.switch_to.window(driver.window_handles[0])
                                return True
                            except Exception as e:
                                logger.warning(f"Не получилось кликнуть на {href}: {e}")
                                continue
                    else:
                        logger.debug(f"Ссылка без href: {result.text}")
            except TimeoutException:
                logger.debug(f"Селектор {selector} не нашёл элементов")
                continue
            except ElementClickInterceptedException as e:
                logger.warning(f"Клик перехвачен для селектора {selector}: {e}")
                continue
        return False

    def _go_to_next_page(self, driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(1.0, 2.0))

        for selector in self.next_page_selectors:
            try:
                method = By.XPATH if selector.startswith('//') else By.CSS_SELECTOR
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((method, selector))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
                next_button.click()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'serp-item')]"))
                )
                logger.info("Перешли на следующую страницу")
                return True
            except TimeoutException:
                continue
        return False
