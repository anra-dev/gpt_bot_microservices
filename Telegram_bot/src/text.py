import settings


HELP_TEXT = (
    f'Этот бот перенаправляет запросы в ChatGPT.\n'
    f'Режим работы бота: тестовый\n'
    f'Версия телеграмм бота: {settings.BOT_VERSION}\n'
    f'Версия модели ChatGPT: {settings.OPENAI_MODEL}\n'
    f'Доступно тестовое подключение к YandexGPT\n'
    f'(подключить - /yandex_test_on, отключить - /yandex_test_off)\n'
    f'По всем вопросам обращаться @Andreev_Roman'
)

NEW_TEXT = (
    f'v1.6\n'
    f'- Исправлена ошибка при которой бот мог пропустить сообщение от пользователя.\n'
    f'v1.5\n'
    f'- Тестовое подключение YandexGPT.\n'
    f'v1.4\n'
    f'- Из контекста беседы можно удалить конкретный вопрос-ответ.\n'
    f'v1.3\n'
    f'- Контекст беседы сохраняется при перезапуске сервера.\n'
    f'v1.2\n'
    f'- Каждый пользователь имеет свой контекст. Добавлена кнопка удаления контекста.\n'
    f'v1.1\n'
    f'- Бот помнит контекст разговора и можно задавать уточняющие вопросы. '
    f'В данный момент контекст является общим для всех пользователей.\n'
    f'v1.0\n'
    f'- Базовая реализация вопрос-ответ.'
)

# Buttons label
ABOUT_BUTTON = 'О боте 🤖'
NEWS_BUTTON = 'Что нового? 📬'
DELETE_CONTEXT_BUTTON = "Удалить контекст ❌"
SEND_ALL = 'Отправить всем! ⏩'
EXIT = 'Выйти 🔚'
ALL_BUTTONS = [
    ABOUT_BUTTON,
    NEWS_BUTTON,
    DELETE_CONTEXT_BUTTON,
    SEND_ALL,
]
# Inline
DELETE_MESSAGE_BUTTON = "Удалить ❌"
RECOVER_MESSAGE_BUTTON = "Восстановить ✅"

# Messages
WELCOME_TEXT = 'Добро пожаловать!'
UPDATE_KEYBOARD = 'Вы ввели устаревшую команду. Клавиатура обновлена!'
DELETE_MESSAGE_SUCCESS = 'Сообщение удалено из контекста.'
DELETE_MESSAGE_FAILURE = 'Сообщение не найдено.'
DELETE_CONTEXT_SUCCESS = 'Контекст удален!'
DELETE_CONTEXT_FAILURE = 'Контекст отсутствует.'
ERROR_MESSAGE_FOR_USER = '❗Ой! Произошла ошибка. \n🤖 Я уже оповестил администратора.'
LENGTH_EXCEEDED_TEXT = '🤖Превышена длинна контекста. Очистите контекст или удалите часть сообщений.'
ANSWER_MESSAGE = '{answer}\n\n------------\n{model}'
ERROR_MESSAGE_FOR_ADMIN = '❗Error: {error_name};\n❗Chat_id: {chat_id};\n❗Text error: {text_error}'
WRITE_MESSAGE = 'Введите сообщение'

# Тестовые
YANDEX_ON = 'Включено тестирование YandexGPT.'
YANDEX_OFF = 'Тестирование YandexGPT выключено. Используется ChatGPT'

# Admin
WELCOME_ADMIN_TEXT = 'Выберите команду.'
NOT_ADMIN = 'Команда доступна только администраторам.'
EXIT_ADMIN = 'Выход из режима администратора.'
ERROR_ADMIN_MESSAGE = 'Неверный формат сообщения от администратора.'
ADMIN_MAILING_COMPLETED = 'Рассылка завершена.'
