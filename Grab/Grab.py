__author__ = 'ipetrash'


# # Модуль Grab
# # Документация: http://docs.grablib.org/
# # Сайт: http://grablib.org/
# # Репозиторий: https://github.com/lorien/grab
# # Статья: http://habrahabr.ru/post/127584/ и http://habrahabr.ru/post/139435/
# Что такое grab?
# Это библиотека для парсинга сайтов. Её основные функции:
#    Подготовка сетевого запроса (cookies, http-заголовки, POST/GET данные)
#    Запрос на сервер (возможно через HTTP/SOCKS прокси)
#    Получение ответа сервера и его первоначальная обработка (парсинг заголовков, парсинг cookies, определение кодировки документа, обработка редиректа (поддерживаются даже редирект в meta refresh тэге)) Работа с DOM-деревом ответа (если это HTML-документ)
#    Работа с формами (заполнение, автозаполнение)
#    Отладка: логирование процесса в консоль, сетевых запросов и ответов в файлы