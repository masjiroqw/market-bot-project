import os, logging



if not os.path.exists('logs'):
    os.makedirs('logs')

def setup_logger():
    # 1. Создаем логгер
    logger = logging.getLogger("market_bot")
    logger.setLevel(logging.DEBUG)  # Пропускаем всё для начала

    # 2. Формат: Дата [Уровень] Имя: Сообщение
    formatter = logging.Formatter(
        fmt='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 3. Обработчик для консоли (чтобы видеть в PyCharm)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # 4. Обработчик для всех событий (INFO+)
    file_handler = logging.FileHandler("logs/all_activity.log", encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # 5. Обработчик только для ошибок (ERROR+)
    error_handler = logging.FileHandler("logs/errors.log", encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # Добавляем все обработчики к логгеру
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)

    return logger

    