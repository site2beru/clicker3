import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

def setup_browser(user_agent, fingerprint, proxy=None, headless=False, initial_url="https://dzen.ru"):
    options = Options()
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument(f'--window-size={fingerprint["screen_resolution"]}')
    options.add_argument(f'--lang={fingerprint["language"]}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-webrtc')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-notifications')

    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

    if not headless:
        options.headless = False
    options.add_argument(f"user-agent={user_agent}")
    if proxy:
        options.add_argument(f"--proxy-server={proxy}")

    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    logger.info(f"Загружаем начальный URL {initial_url}")
    driver.get(initial_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    current_url = driver.current_url
    domain = urlparse(current_url).hostname
    driver.add_cookie({"name": "session_id", "value": f"session_{random.randint(1000, 9999)}", "domain": domain})
    logger.info(f"Установлен cookie для домена: {domain}")

    return driver