import json
import os
import random
import requests
import logging
from threading import Lock

logger = logging.getLogger(__name__)

class ProxyHandler:
    def __init__(self):
        self.proxy_file = "proxies.json"
        self.working_proxies = []
        self.lock = Lock()

    def get_random_proxy(self):
        with self.lock:
            if not self.working_proxies:
                self._load_proxies()
            return random.choice(self.working_proxies) if self.working_proxies else None

    def _load_proxies(self):
        if not os.path.exists(self.proxy_file):
            logger.error(f"Файл {self.proxy_file} не найден")
            return

        try:
            with open(self.proxy_file, 'r', encoding='utf-8') as f:
                proxy_data = json.load(f)

            if not isinstance(proxy_data, list):
                logger.error("Формат файла proxies.json должен быть списком")
                return

            for proxy in proxy_data:
                ip, port = proxy.get('ip_address'), proxy.get('port')
                if ip and port and self._check_proxy(f"{ip}:{port}"):
                    self.working_proxies.append(f"{ip}:{port}")
        except Exception as e:
            logger.error(f"Ошибка загрузки прокси: {e}")

    def _check_proxy(self, proxy):
        try:
            response = requests.get("https://ya.ru", proxies={"http": proxy, "https": proxy}, timeout=5)
            return response.status_code == 200
        except:
            return False

proxy_handler = ProxyHandler()

def get_random_proxy():
    return proxy_handler.get_random_proxy()