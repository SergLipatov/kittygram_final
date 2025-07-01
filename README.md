#Kittygram [![CI/CD](https://github.com/SergLipatov/kittygram_final/actions/workflows/main.yml/badge.svg)](https://github.com/SergLipatov/kittygram_final/actions)
Kittygram - это fullstack-приложение для обмена фотографиями котиков, построенное на основе современных технологий. Проект реализован с использованием Docker-контейнеров для обеспечения переносимости и простоты развёртывания.

## Технологический стек

**Backend:**
- Python 3.9
- Django 3.2
- Django REST Framework
- PostgreSQL
- Gunicorn
- Nginx (реверс-прокси)

**Frontend:**
- React
- Node.js 18

**Инфраструктура:**
- Docker
- Docker Compose
- GitHub Actions (CI/CD)

**Тестирование:**
- pytest
- Flake8 (линтер)
- React Testing Library

## Структура проекта

```
kittygram_final/
├── backend/          # Django-приложение
│   ├── cats/         # Модуль с API для котиков
│   ├── kittygram_backend/  # Основные настройки Django
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/         # React-приложение
│   ├── Dockerfile
│   ├── package.json
│   └── src/          # Исходный код фронтенда
├── nginx/            # Конфигурация Nginx
├── .github/
│   └── workflows/    # GitHub Actions для CI/CD
├── docker-compose.yml        # Конфигурация для разработки
├── docker-compose.production.yml # Продакшн-конфигурация
└── .env.example      # Шаблон переменных окружения
```

## Установка и запуск

### Требования
- Docker
- Docker Compose

### Шаги для запуска

1. **Клонирование репозитория:**
   ```bash
   git clone https://github.com/SegLipatov/kittygram_final.git
   cd kittygram_final
   ```

3. **Настройка переменных окружения:**
   - Создайте файл `.env` на основе `.env.example`
   - Заполните необходимые значения:
     ```env
     POSTGRES_DB=kittygram_db
     POSTGRES_USER=kittygram_user
     POSTGRES_PASSWORD=ваш_сложный_пароль
     SECRET_KEY=ваш_секретный_ключ_django
     ALLOWED_HOSTS=localhost,127.0.0.1,backend
     DEBUG=True  # Для разработки
     ```

- **Важно для продакшн:** При деплое на сервер скопируйте `.env` файл вручную в корень проекта на сервере

2. **Запуск в режиме разработки:**
   ```bash
   docker-compose up --build
   ```
   Приложение будет доступно по адресу: `http://localhost:9000`

3. **Запуск в продакшн-режиме:**
   ```bash
   docker-compose -f docker-compose.production.yml up --build -d
   ```

4. **Выполнение миграций и сбор статики:**
   ```bash
   docker-compose -f docker-compose.production.yml exec backend python manage.py migrate
   docker-compose -f docker-compose.production.yml exec backend python manage.py collectstatic
   ```

## Настройка CI/CD

Проект включает готовый workflow для GitHub Actions, который выполняет:
1. Тестирование backend и фронтенда
2. Сборку Docker-образов
3. Публикацию образов на Docker Hub
4. Деплой на сервер

### Необходимые секреты в GitHub:
- `DOCKER_USERNAME` - логин Docker Hub
- `DOCKER_PASSWORD` - пароль Docker Hub
- `HOST` - IP сервера
- `USER` - пользователь SSH
- `SSH_KEY` - приватный ключ
- `SSH_PASSPHRASE` - пароль для ключа (если есть)
- `TELEGRAM_TOKEN` - токен бота для уведомлений
- `TELEGRAM_TO` - ID чата для уведомлений

## Важные файлы конфигурации

### Nginx (nginx/nginx.conf)
Конфигурация реверс-прокси, которая:
- Обслуживает статические файлы фронтенда
- Проксирует API-запросы на бэкенд
- Настраивает кэширование

### Docker Compose (docker-compose.yml)
Описывает сервисы:
1. `db` - PostgreSQL
2. `backend` - Django-приложение
3. `frontend` - React-приложение
4. `gateway` - Nginx

### GitHub Actions (.github/workflows/main.yml)
Автоматизирует:
- Запуск тестов
- Сборку образов
- Деплой на сервер
- Отправку уведомлений в Telegram

## Разработка

### Запуск тестов
Backend-тесты:
```bash
docker-compose exec backend python manage.py test
```

Frontend-тесты:
```bash
docker-compose exec frontend npm test
```

### Линтинг кода
```bash
docker-compose exec backend flake8 .
```

## Возможные проблемы

1. **Ошибки подключения к базе данных:**
   - Убедитесь, что в `.env` правильно указаны параметры DB_HOST, DB_PORT
   - Проверьте, что контейнер PostgreSQL запущен

2. **Проблемы со сборкой фронтенда:**
   - Удалите кэш Docker: `docker system prune -a`
   - Пересоберите образы: `docker-compose build --no-cache frontend`

3. **Ошибки CORS:**
   - Убедитесь, что в `ALLOWED_HOSTS` указаны правильные хосты
   - Проверьте конфигурацию Nginx

## Автор

[SegLipatov](https://github.com/SegLipatov) - разработчик и создатель Kittygram

[](https://github.com/SegLipatov)[https://img.shields.io/badge/GitHub-SegLipatov-blue?style=flat&logo=github](https://img.shields.io/badge/GitHub-SegLipatov-blue?style=flat&logo=github)
