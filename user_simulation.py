from fake_useragent import UserAgent
import random

def get_random_mobile_user_agent():
    ua = UserAgent()
    # Получаем список Chrome user-agents и фильтруем только мобильные
    chrome_agents = ua.chrome
    attempts = 0
    max_attempts = 10
    while attempts < max_attempts:
        agent = ua.chrome  # Получаем случайный Chrome user-agent
        if 'Mobile' in agent:  # Проверяем, является ли он мобильным
            return agent
        attempts += 1
    # Если не нашли мобильный за max_attempts, возвращаем любой мобильный по умолчанию
    return "Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36"

def get_random_fingerprint():
    screen_resolutions = [
        "320x480", "360x640", "375x667", "414x896"
    ]
    return {
        "screen_resolution": random.choice(screen_resolutions),
        "language": random.choice(["ru-RU", "ru"]),
        "platform": random.choice(["Linux armv8l", "Linux armv7l", "iPhone"])
    }