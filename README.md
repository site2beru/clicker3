13.03.2025 usp
чудо-бот для захода на сайты через Яшу (с помощью Дзена) по заданным поисковым запросам
используем прокси (если нужно), куки и фингерпринты

алгоритм действий следующий:

1. открываем браузер, заходим на яндекс (через dzen.ru)
2. устанавливаем cookie для сайта и заходим снова
3. находим iframe с поиском Яндекса, а внутри него поисковую строку
4. пишем в строку ключевик и жмем Enter
5. ищем нужный нам сайт (задается в конце файла)
6. тыкаем на него и сразу сваливаем
7. ждем N-ное время и идем еще раз

main — этот файл — исполняет запуск
proxy_handler — настройки прокси
browser_config — конфигурация
website_visitor — процесс поиска по страницам
user_simulation – настройки девайса пользователя

комменты для headless

14.03.2025 — добавлена проверка библиотек

note: с проверкой на робота случаются проблемы
