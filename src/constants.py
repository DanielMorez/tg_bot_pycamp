# Константы для callback_data
CALLBACK_AUTH = "auth"
CALLBACK_FAQ = "faq"
CALLBACK_FAQ_THEME = "faq_theme"
CALLBACK_FAQ_QUESTION = "faq_question"
CALLBACK_FAQ_BACK = "faq_back"
CALLBACK_FAQ_HOME = "faq_home"

# Ключи для кеша Redis
CACHE_PHONE_PREFIX = "phone:"
CACHE_AUTH_LINK_PREFIX = "auth_link:"

# Тексты кнопок
BUTTON_AUTH = "🔐Авторизоваться"
BUTTON_SUPPORT = "💬Чат с поддержкой"
BUTTON_CHANNEL = "💜Наш канал"
BUTTON_FAQ = "⁉️Вопросы и ответы"
BUTTON_AUTH_LINK = "🔑 Ссылка для авторизации"
BUTTON_SHARE_PHONE = "Поделиться номером телефона 📱"
BUTTON_FAQ_BACK = "⬅️ Назад"
BUTTON_FAQ_HOME = "🏠 Главное меню"


# Состояния FSM
class AuthState:
    WAITING_FOR_PHONE = "waiting_for_phone"
