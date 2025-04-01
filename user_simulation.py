import random

# Список реальных мобильных User-Agent для Android
MOBILE_USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 11; SM-A505F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36"
]

def get_random_mobile_user_agent():
    return random.choice(MOBILE_USER_AGENTS)

def get_random_fingerprint():
    screen_resolutions = [
        "360x640",  # HD
        #"360x800",  # HD+
        "412x732",  # FHD
        "360x780"   # Custom Android resolution
    ]
    return {
        "screen_resolution": random.choice(screen_resolutions),
        "language": "ru-RU",
        "platform": "Linux armv8l"  # Типичная платформа для Android 11
    }
