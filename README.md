# Authentication Service - OutOfBoxSystems

Высокопроизводительный сервис аутентификации с поддержкой традиционного логина по email/паролю и социальных сетей (Google, Facebook, Twitter). Построен на FastAPI с акцентом на безопасность, масштабируемость и лучший пользовательский опыт.

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-red.svg)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

## 📋 Содержание

- [Возможности](#-возможности)
- [Быстрый старт](#-быстрый-старт)
- [Установка и настройка](#-установка-и-настройка)
- [Использование](#-использование)
- [API Документация](#-api-документация)
- [Тестирование](#-тестирование)
- [Архитектура](#-архитектура)
- [Безопасность](#-безопасность)
- [Видео демонстрация](#-видео-демонстрация)
- [Разработка](#-разработка)
- [Деплой в продакшн](#-деплой-в-продакшн)

## ✨ Возможности

### Аутентификация

- ✅ **Email/Password аутентификация** с безопасным хешированием паролей (bcrypt)
- ✅ **Social Login** (Google, Facebook, Twitter) через OAuth 2.0
- ✅ **JWT токены** для stateless аутентификации
- ✅ **Refresh токены** для поддержания сессий
- ✅ **Single Sign-On (SSO)** - вход на нескольких устройствах

### Безопасность

- 🔒 **Защита от CSRF, XSS** через security headers
- 🔒 **Rate limiting** для защиты от brute force атак
- 🔒 **CORS policy** для контроля доступа
- 🔒 **Безопасное хранение паролей** (bcrypt с солью)
- 🔒 **Защита от SQL injection** (SQLAlchemy ORM)
- 🔒 **OAuth 2.0 best practices**

### Технические возможности

- ⚡ **Async/await** для высокой производительности
- ⚡ **Горизонтальное масштабирование** (stateless design)
- ⚡ **Автоматическая документация API** (Swagger/ReDoc)
- ⚡ **Интеграционные тесты** с pytest
- ⚡ **Docker Compose** для локальной разработки
- ⚡ **Makefile** для автоматизации задач

## 🚀 Быстрый старт

### Предварительные требования

Убедитесь, что установлены следующие инструменты:

- **Python 3.13+** - [Скачать](https://www.python.org/downloads/)
- **uv** - [Скачать](https://docs.astral.sh/uv/getting-started/installation/)
- **Docker & Docker Compose** - [Скачать](https://www.docker.com/products/docker-desktop/)
- **Make** (опционально, для использования Makefile)
- **Git**

### Запуск за 3 шага

```bash
# 1. Клонировать репозиторий
git clone <repository-url>
cd TestTask

# 2. Настроить проект (установка зависимостей + создание .env)
make setup

# 3. Проверить готовность окружения
make doctor

# 4. Запустить сервис
make up
```

### Локальная разработка (без Docker)

```bash
# Запуск с автоперезагрузкой
make run-dev

# Запуск без автоперезагрузки (как в продакшене)
make run-local
```

Сервис будет доступен по адресу:
- **API**: http://localhost:8000
- **Документация (Swagger)**: http://localhost:8000/docs
- **Альтернативная документация (ReDoc)**: http://localhost:8000/redoc

## 🎯 Полезные команды Makefile

### Основные команды разработки

```bash
# Настройка проекта
make setup          # Установка зависимостей + создание .env
make doctor         # Диагностика окружения
make install-deps   # Обновление зависимостей

# Запуск приложения
make run-dev        # Разработка с автоперезагрузкой
make run-local      # Запуск без автоперезагрузки (как в продакшене)

# Docker команды
make up             # Запуск всех сервисов
make down           # Остановка сервисов
make rebuild        # Полная перестройка (clean + build + up)
make logs           # Просмотр логов
make status         # Статус сервисов
```

### База данных

```bash
# Миграции
make migrate        # Применить миграции (alias для migrate-up)
make migrate-create name=add_new_field  # Создать новую миграцию
make migrate-down   # Откатить последнюю миграцию

# Управление БД
make db-reset       # Сброс базы данных (⚠️ удаляет все данные!)
make db-shell       # Подключение к PostgreSQL
```

### Утилиты

```bash
# Код
make format         # Форматирование кода (black + isort)
make lint           # Проверка кода (flake8)

# Очистка
make clean          # Очистка проекта и Docker
make prune          # Удаление всех Docker данных (⚠️ опасно!)

# Тестирование API
make test-auth      # Тестирование аутентификации
make test-google-oauth  # Тестирование Google OAuth
make health         # Проверка здоровья сервиса
```

### Полный список команд

```bash
make help           # Показать все доступные команды
```

## 📦 Установка и настройка

### Вариант 1: Docker Compose (рекомендуется)

Это самый простой способ для локальной разработки и тестирования.

```bash
# Собрать Docker образы
make build

# Запустить все сервисы (app, database, redis)
make up

# Посмотреть логи
make logs

# Остановить сервисы
make down
```

### Вариант 2: Локальная установка

Для разработки с hot reload и отладкой.

```bash
# Установить зависимости
make dev-install

# Запустить PostgreSQL и Redis через Docker Compose
docker-compose up -d db redis

# Создать файл .env
cat > .env << EOF
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/auth_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-super-secret-key-change-this-in-production
DEBUG=true
LOG_LEVEL=INFO
EOF

# Запустить приложение в режиме разработки
make run-dev
```

### Конфигурация

#### Переменные окружения

Создайте файл `.env` в корне проекта:

```env
# Основные настройки
APP_NAME="Sales Platform Auth Service"
DEBUG=false
LOG_LEVEL=INFO

# Безопасность - ОБЯЗАТЕЛЬНО ИЗМЕНИТЕ В ПРОДАКШЕНЕ!
SECRET_KEY=your-super-secret-key-change-this-in-production-minimum-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# База данных
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/auth_db

# Redis
REDIS_URL=redis://redis:6379/0

# CORS
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:8000"]

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback

# Facebook OAuth
FACEBOOK_CLIENT_ID=your-facebook-client-id
FACEBOOK_CLIENT_SECRET=your-facebook-client-secret
FACEBOOK_REDIRECT_URI=http://localhost:8000/api/v1/auth/facebook/callback

# Twitter OAuth
TWITTER_CLIENT_ID=your-twitter-client-id
TWITTER_CLIENT_SECRET=your-twitter-client-secret
TWITTER_REDIRECT_URI=http://localhost:8000/api/v1/auth/twitter/callback

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
```

#### Настройка OAuth провайдеров

**Google OAuth**:
1. Перейти в [Google Cloud Console](https://console.cloud.google.com/)
2. Создать новый проект или выбрать существующий
3. Включить Google+ API
4. Создать OAuth 2.0 Client ID (Web application)
5. Добавить redirect URI: `http://localhost:8000/api/v1/auth/google/callback`
6. Скопировать Client ID и Client Secret в `.env`

**Facebook OAuth**:
1. Перейти в [Facebook Developers](https://developers.facebook.com/)
2. Создать новое приложение
3. Добавить Facebook Login product
4. Настроить Valid OAuth Redirect URIs: `http://localhost:8000/api/v1/auth/facebook/callback`
5. Скопировать App ID и App Secret в `.env`

**Twitter OAuth**:
1. Перейти в [Twitter Developer Portal](https://developer.twitter.com/)
2. Создать новое приложение
3. Включить OAuth 2.0
4. Добавить callback URL: `http://localhost:8000/api/v1/auth/twitter/callback`
5. Скопировать Client ID и Client Secret в `.env`

## 💻 Использование

### Регистрация нового пользователя

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "full_name": "John Doe"
  }'
```

**Ответ**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "is_active": true
  }
}
```

### Вход по email и паролю

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### Получение информации о пользователе

```bash
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Обновление токена

```bash
curl -X POST "http://localhost:8000/api/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "YOUR_REFRESH_TOKEN"
  }'
```

### Социальный логин (Google)

1. Получить URL авторизации:
```bash
curl -X GET "http://localhost:8000/api/v1/auth/google"
```

2. Перенаправить пользователя на `authorization_url` из ответа

3. После авторизации Google перенаправит на callback URL с кодом

4. Сервис автоматически обменяет код на токены и вернет JWT токены

## 📚 API Документация

### Интерактивная документация

После запуска сервиса доступны две версии документации:

- **Swagger UI**: http://localhost:8000/docs
  - Интерактивное тестирование API
  - Можно отправлять запросы прямо из браузера

- **ReDoc**: http://localhost:8000/redoc
  - Красивая документация для чтения
  - Экспорт в OpenAPI спецификацию

### Основные эндпоинты

#### Аутентификация

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/api/v1/auth/register` | Регистрация нового пользователя |
| POST | `/api/v1/auth/login` | Вход по email/паролю |
| POST | `/api/v1/auth/refresh` | Обновление токена |
| GET | `/api/v1/auth/google` | Начать Google OAuth |
| GET | `/api/v1/auth/google/callback` | Google OAuth callback |
| GET | `/api/v1/auth/facebook` | Начать Facebook OAuth |
| GET | `/api/v1/auth/facebook/callback` | Facebook OAuth callback |
| GET | `/api/v1/auth/twitter` | Начать Twitter OAuth |
| GET | `/api/v1/auth/twitter/callback` | Twitter OAuth callback |

#### Пользователи

| Метод | Эндпоинт | Описание | Требует авторизации |
|-------|----------|----------|---------------------|
| GET | `/api/v1/users/me` | Получить профиль текущего пользователя | ✅ |
| GET | `/api/v1/users/profile` | Alias для `/me` | ✅ |

#### Системные

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/` | Root endpoint с информацией о сервисе |
| GET | `/health` | Health check для мониторинга |

### Схемы данных

Подробные схемы запросов и ответов доступны в Swagger UI.

## 🧪 Тестирование

### Запуск всех тестов

```bash
# В Docker контейнере (рекомендуется)
make test

# Локально (требуется настроенная БД)
make test-local
```

### Запуск интеграционных тестов

```bash
make test-integration
```

### Покрытие кода

После запуска тестов HTML отчет о покрытии доступен в `htmlcov/index.html`

```bash
# Открыть отчет о покрытии
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Структура тестов

```
tests/
├── __init__.py
├── conftest.py          # Fixtures и конфигурация
└── integration/
    ├── __init__.py
    └── test_auth.py     # Интеграционные тесты аутентификации
```

### Покрытые сценарии

- ✅ Успешная регистрация
- ✅ Регистрация с дублирующимся email
- ✅ Валидация email и пароля
- ✅ Успешный вход
- ✅ Вход с неверным паролем
- ✅ Обновление токенов
- ✅ Получение профиля пользователя
- ✅ Авторизация с недействительным токеном

## 🏗 Архитектура

### Высокоуровневая архитектура

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────────┐
│   FastAPI App   │
│  ┌───────────┐  │
│  │Middleware │  │  - CORS, Security Headers, Rate Limiting
│  └───────────┘  │
│  ┌───────────┐  │
│  │ API Layer │  │  - REST endpoints
│  └───────────┘  │
│  ┌───────────┐  │
│  │ Services  │  │  - Business logic
│  └───────────┘  │
│  ┌───────────┐  │
│  │   Models  │  │  - Database models
│  └───────────┘  │
└────┬──────┬─────┘
     │      │
     ▼      ▼
┌─────────┐ ┌──────┐
│PostgreSQL│ │Redis │
└─────────┘ └──────┘
```

### Структура проекта

```
TestTask/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py    # FastAPI dependencies
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py         # Аутентификация endpoints
│   │       └── users.py        # Пользовательские endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Конфигурация приложения
│   │   ├── security.py         # JWT, password hashing
│   │   └── database.py         # Database connection
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py             # User & SocialAccount models
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py             # User Pydantic schemas
│   │   └── auth.py             # Auth Pydantic schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py     # User business logic
│   │   └── oauth_service.py    # OAuth providers logic
│   └── utils/
│       ├── __init__.py
│       └── middleware.py       # Custom middleware
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── integration/
│       └── test_auth.py
├── docker/                     # Docker-related files
├── main.py                     # Application entry point
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Docker Compose configuration
├── pyproject.toml              # Python dependencies
├── Makefile                    # Automation commands
├── README.md                   # This file
└── DESIGN.md                   # Detailed design document
```

### Технологический стек

- **Backend**: Python 3.13, FastAPI 0.115+
- **Database**: PostgreSQL 16 with asyncpg
- **Cache**: Redis 7
- **ORM**: SQLAlchemy 2.0+ (async)
- **Authentication**: JWT (python-jose), OAuth 2.0 (Authlib)
- **Password Hashing**: bcrypt (passlib)
- **Testing**: pytest, pytest-asyncio
- **Containerization**: Docker, Docker Compose
- **ASGI Server**: Uvicorn

## 🔒 Безопасность

### Реализованные меры безопасности

1. **Password Security**
   - Bcrypt hashing с автоматической генерацией соли
   - Минимальная длина пароля 8 символов
   - Пароли никогда не сохраняются в открытом виде

2. **JWT Security**
   - Короткий lifetime для access токенов (30 минут)
   - Длинный lifetime для refresh токенов (7 дней)
   - Подпись токенов с использованием секретного ключа
   - Разделение типов токенов (access vs refresh)

3. **OAuth Security**
   - OAuth 2.0 authorization code flow
   - State parameter для защиты от CSRF
   - Валидация redirect URI

4. **HTTP Security Headers**
   - X-Frame-Options: DENY
   - X-Content-Type-Options: nosniff
   - X-XSS-Protection: 1; mode=block
   - Strict-Transport-Security

5. **Rate Limiting**
   - 60 запросов в минуту по умолчанию
   - Защита от brute force атак

6. **CORS Policy**
   - Whitelist разрешенных origin'ов
   - Контроль методов и заголовков

7. **Input Validation**
   - Pydantic schemas для валидации
   - Type checking на уровне Python

8. **SQL Injection Protection**
   - SQLAlchemy ORM с параметризованными запросами
   - Нет raw SQL с конкатенацией строк

### Рекомендации для продакшена

См. раздел [Деплой в продакшн](#-деплой-в-продакшн) и документ [DESIGN.md](DESIGN.md).

## 🎥 Видео демонстрация

### Инструкции для записи видео

**Что должно быть продемонстрировано**:

1. **Запуск сервиса**:
   ```bash
   make build
   make up
   ```

2. **Проверка работоспособности**:
   - Открыть http://localhost:8000/health
   - Показать http://localhost:8000/docs

3. **Регистрация нового пользователя** (через Postman/Insomnia/curl):
   - Отправить POST запрос на `/api/v1/auth/register`
   - Показать полученные токены

4. **Вход существующего пользователя**:
   - Отправить POST запрос на `/api/v1/auth/login`
   - Показать успешный ответ с токенами

5. **Получение профиля**:
   - Использовать access token из предыдущего шага
   - GET запрос на `/api/v1/users/me` с Authorization header
   - Показать данные пользователя

6. **Обновление токена**:
   - POST запрос на `/api/v1/auth/refresh`
   - Показать новые токены

7. **Попытка доступа с недействительным токеном**:
   - GET запрос на `/api/v1/users/me` с неверным токеном
   - Показать ошибку 401

8. **Запуск тестов**:
   ```bash
   make test
   ```
   - Показать успешное выполнение всех тестов

9. **Объяснение процесса**:
   - Рассказать о каждом шаге
   - Объяснить что происходит под капотом
   - Показать структуру проекта

**Рекомендуемые инструменты для записи**:
- **Postman**: Удобный GUI для тестирования API
- **Insomnia**: Альтернатива Postman
- **curl + jq**: Командная строка (для продвинутых)
- **Screen recording**: OBS Studio, Loom, QuickTime (macOS)

**Длительность**: 5-10 минут

**Формат видео**: MP4, MOV, или ссылка на YouTube/Loom

## 🛠 Разработка

### Доступные команды Make

```bash
make help              # Показать все доступные команды
make check-deps        # Проверить зависимости
make install           # Установить production зависимости
make dev-install       # Установить dev зависимости
make setup             # Полная настройка проекта
make build             # Собрать Docker образы
make up                # Запустить все сервисы
make down              # Остановить сервисы
make down-v            # Остановить и удалить volumes
make logs              # Показать логи всех сервисов
make logs-app          # Показать логи приложения
make test              # Запустить тесты в Docker
make test-local        # Запустить тесты локально
make test-integration  # Запустить интеграционные тесты
make clean             # Очистить временные файлы
make shell             # Открыть shell в контейнере
make db-shell          # Открыть PostgreSQL shell
make run-dev           # Запустить в режиме разработки
make dev               # Alias для up
make status            # Показать статус сервисов
make restart           # Перезапустить сервисы
make health            # Проверить здоровье приложения
```

### Hot Reload

Для разработки с автоматической перезагрузкой:

```bash
make run-dev
```

Приложение будет перезагружаться при изменении файлов.

### Подключение к базе данных

```bash
# Через Docker
make db-shell

# Напрямую (если PostgreSQL запущен локально)
psql -U postgres -d auth_db
```

### Логи

```bash
# Все сервисы
make logs

# Только приложение
make logs-app

# Только база данных
docker-compose logs -f db
```

## 🚀 Деплой в продакшн

### Подготовка к продакшену

1. **Сгенерировать надежный SECRET_KEY**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

2. **Настроить переменные окружения**:
   - Использовать Secrets Manager (AWS Secrets Manager, GCP Secret Manager)
   - Никогда не коммитить `.env` файлы

3. **Настроить HTTPS**:
   - SSL/TLS сертификаты (Let's Encrypt, AWS Certificate Manager)
   - Настроить редирект HTTP → HTTPS

4. **Настроить OAuth redirect URIs**:
   - Обновить redirect URIs в консолях OAuth провайдеров
   - Использовать production домены

5. **Database**:
   - Использовать managed PostgreSQL (AWS RDS, Google Cloud SQL)
   - Настроить backups
   - Настроить репликацию для читающих реплик

6. **Redis**:
   - Использовать managed Redis (AWS ElastiCache, GCP Memorystore)
   - Настроить persistence

7. **Мониторинг**:
   - Настроить логирование (CloudWatch, Stackdriver, ELK)
   - Настроить метрики (Prometheus, Datadog)
   - Настроить алерты

### Deployment опции

**Docker Compose (простые деплои)**:
```bash
# На сервере
docker-compose -f docker-compose.prod.yml up -d
```

**Kubernetes** (масштабируемые деплои):
- Создать Kubernetes manifests
- Использовать Helm charts
- Настроить ingress controller

**Cloud Platforms**:
- **AWS**: ECS/Fargate + RDS + ElastiCache
- **Google Cloud**: Cloud Run + Cloud SQL + Memorystore
- **Azure**: App Service + Azure Database + Azure Cache

### Checklist продакшн-готовности

- [ ] SECRET_KEY сгенерирован и сохранен в Secrets Manager
- [ ] DEBUG=false
- [ ] HTTPS настроен и принудителен
- [ ] OAuth credentials настроены для продакшен-доменов
- [ ] Database backups настроены
- [ ] Мониторинг и логирование настроены
- [ ] Health checks настроены
- [ ] Rate limiting настроен
- [ ] CORS настроен для правильных origin'ов
- [ ] Email верификация реализована (опционально)
- [ ] Password reset реализован (опционально)
- [ ] 2FA настроен (опционально)

## 📝 Лицензия

Этот проект создан как тестовое задание для компании OutOfBoxSystems.

## 🤝 Контакты

Для вопросов по проекту обращайтесь к автору.

---

## 📖 Дополнительная документация

- [DESIGN.md](DESIGN.md) - Подробная архитектурная документация
- [API Documentation](http://localhost:8000/docs) - После запуска сервиса

---

**Создано с ❤️ используя FastAPI**

