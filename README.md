# Telegram Bot - Duginov.Courses

Telegram бот для авторизации пользователей и получения доступа к образовательным материалам курсов программирования Duginov Courses.

## Описание

Бот предоставляет следующие возможности:
- 🔐 Авторизация пользователей через номер телефона
- 🔗 Генерация временных ссылок для доступа к материалам курса
- 💬 Интеграция с чатом поддержки
- 📢 Уведомления о важных событиях и дедлайнах
- 🦊 Связь с официальным каналом

## Технический стек

### Backend
- **Python 3.9+** - основной язык разработки
- **aiogram 3.x** - фреймворк для Telegram ботов
- **Redis** - кеширование данных пользователей
- **aiohttp** - асинхронные HTTP запросы к API
- **Pydantic** - валидация данных и настройки

### Инфраструктура
- **Docker** - контейнеризация приложения
- **Docker Compose** - оркестрация сервисов
- **Redis** - база данных для кеширования

### Инструменты разработки
- **Ruff** - быстрый линтер и форматтер на Rust
- **MyPy** - статическая типизация
- **Pytest** - тестирование
- **Pre-commit** - автоматические проверки перед коммитом

## Установка и запуск

### Предварительные требования
- Python 3.9 или выше
- Docker и Docker Compose
- Redis сервер

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd tg_bot_pycamp
```

### 2. Настройка переменных окружения
Создайте файл `.env` в корневой директории проекта:

```env
# Основные настройки бота
BOT_TOKEN=your_telegram_bot_token_here
REDIS_URL=redis://localhost:6379/0

# API настройки
API_BASE_URL=https://api.codelis.com
API_LOGIN=your_api_username
API_PASSWORD=your_api_password

# Настройки UI (опционально)
SUPPORT_BOT_URL=https://t.me/your_support_bot
CHANNEL_URL=https://t.me/codelis_digest
LOADING_STICKER_ID=CAACAgIAAxkBAAExqU9nq5ox8OKuKAR3gVTbqlxsOocsYAACeBsAArZjKElJPqq2J-v4QTYE

# Настройки кеширования (опционально)
PHONE_CACHE_TTL=604800  # 7 дней в секундах
AUTH_LINK_CACHE_TTL=600  # 10 минут в секундах

# Сообщения об ошибках (опционально)
API_ERROR_MESSAGE=Наш сервис сейчас немного прилёг отдохнуть — мы быстро чиним и перезагружаем, чтобы всё снова работало как часы🤕
LOADING_MESSAGE=Генерируем ссылку...
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Запуск с Docker (рекомендуется)

#### Запуск всех сервисов
```bash
docker-compose up -d
```

#### Запуск только бота
```bash
docker-compose up bot
```

### 5. Запуск без Docker

#### Запуск Redis
```bash
# macOS (с Homebrew)
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis-server

# Windows
# Установите Redis через WSL или используйте Docker
```

#### Запуск бота
```bash
python bot.py
```

## Структура проекта

```
tg_bot_pycamp/
├── bot.py                    # Точка входа приложения
├── config.py                 # Конфигурация и настройки
├── requirements.txt          # Зависимости Python
├── docker-compose.yaml       # Docker Compose конфигурация
├── Dockerfile               # Docker образ
├── .env                     # Переменные окружения (создать)
├── README.md               # Документация
└── src/
    ├── constants.py         # Константы проекта
    ├── exceptions.py        # Исключения
    ├── types.py            # Типы данных
    ├── handlers/
    │   └── start.py        # Обработчики команд
    ├── services/
    │   ├── auth_service.py # Сервис авторизации
    │   ├── ui_service.py   # Сервис UI
    │   ├── message_service.py # Сервис сообщений
    │   ├── cache.py        # Сервис кеширования
    │   ├── auth.py         # API авторизации
    │   └── api_client.py   # API клиент
    ├── utils/
    │   ├── logger.py       # Утилиты логирования
    │   └── readable_time.py # Утилиты времени
    └── keyboards/
        └── messages.py     # Тексты сообщений
```

## Разработка

### Установка для разработки
```bash
# Клонирование репозитория
git clone <repository-url>
cd tg_bot_pycamp

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/macOS
# или
venv\Scripts\activate      # Windows

# Установка зависимостей
pip install -r requirements.txt

# Установка дополнительных зависимостей для разработки
pip install -r requirements-dev.txt  # если есть

# Или используйте Makefile
make install-dev
```

### Полезные команды Makefile
```bash
make help          # Показать все доступные команды
make install-dev   # Установить зависимости для разработки
make test          # Запустить тесты
make test-cov      # Запустить тесты с покрытием
make lint-fix      # Исправить проблемы с кодом
make format        # Отформатировать код
make check         # Проверить типы
make check-all     # Запустить все проверки
make clean         # Очистить кеш и временные файлы
make run           # Запустить бота
make docker-run    # Запустить с помощью Docker
```

### Запуск тестов
```bash
python -m pytest tests/
```

### Линтинг и форматирование
```bash
# Проверка и исправление кода с помощью Ruff
ruff check src/ tests/
ruff check --fix src/ tests/

# Форматирование кода
ruff format src/ tests/

# Проверка типов
mypy src/

# Или используйте Makefile для удобства
make lint-fix    # Исправить проблемы с кодом
make format      # Отформатировать код
make check       # Проверить типы
make check-all   # Запустить все проверки
```

## API интеграция

Бот интегрируется с внешним API для авторизации пользователей:

### Endpoints
- `POST /api/v1/accounts/login` - авторизация пользователя

### Параметры запроса
```json
{
    "telegram_user_id": "123456789",
    "telegram_username": "username",
    "phone": "+79001234567"
}
```

### Ответ API
```json
{
    "authorization_link": "https://app.codelis.com/auth?token=abc123",
    "expires_at": 1640995200
}
```

## Кеширование

Бот использует Redis для кеширования:

### Кешируемые данные
- **Номер телефона**: 7 дней
- **Ссылка авторизации**: 10 минут

### Ключи кеша
- `phone:{user_id}` - номер телефона пользователя
- `auth_link:{user_id}` - ссылка авторизации с временем истечения

## Мониторинг и логирование

### Уровни логирования
- **INFO**: Основные действия пользователей
- **ERROR**: Ошибки и исключения
- **WARNING**: Предупреждения (например, недоступность Redis)

### Структурированное логирование
```python
# Пример лога
User(id=123456789, username=john_doe) started bot
User(id=123456789, username=john_doe) requested auth
User(id=123456789, username=john_doe) shared phone phone=+79001234567
```

## Развертывание

### Production окружение
1. Настройте переменные окружения для production
2. Используйте Docker Compose для развертывания
3. Настройте мониторинг и логирование
4. Настройте резервное копирование Redis

### Пример docker-compose.prod.yaml
```yaml
version: '3.8'
services:
  bot:
    build: .
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
      - REDIS_URL=${REDIS_URL}
      - API_BASE_URL=${API_BASE_URL}
      - API_LOGIN=${API_LOGIN}
      - API_PASSWORD=${API_PASSWORD}
    restart: unless-stopped
    depends_on:
      - redis
  
  redis:
    image: redis:7-alpine
    restart: unless-stopped
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

volumes:
  redis_data:
```

## Безопасность

### Рекомендации
- Используйте сильные пароли для API
- Ограничьте доступ к Redis
- Регулярно обновляйте зависимости
- Мониторьте логи на предмет подозрительной активности
- Используйте HTTPS для API запросов

## Поддержка

### Полезные команды
```bash
# Просмотр логов
docker-compose logs -f bot

# Перезапуск сервиса
docker-compose restart bot

# Проверка статуса
docker-compose ps

# Очистка кеша Redis
docker-compose exec redis redis-cli FLUSHALL
```

### Контакты
- Поддержка: [@your_support_bot](https://t.me/your_support_bot)
- Канал: [@codelis_digest](https://t.me/codelis_digest)

## Лицензия

MIT License - см. файл LICENSE для деталей.
