# YaCut — сервис сокращения ссылок и загрузки файлов

YaCut — это веб-приложение на Flask для создания коротких ссылок и загрузки файлов с генерацией коротких URL.  
Также доступно REST API для интеграции с внешними сервисами.

---

## 🚀 Возможности

- Сокращение длинных URL
- Пользовательские короткие идентификаторы
- REST API для создания и получения ссылок
- Загрузка файлов на Яндекс.Диск с генерацией коротких ссылок
- Автоматическая генерация уникальных коротких ID
- Обработка ошибок 404 и 500

---

## 🧱 Технологии

- Python 3.12+
- Flask
- SQLAlchemy
- Flask-Migrate
- Flask-WTF
- SQLite (по умолчанию)
- aiohttp (асинхронная загрузка файлов)
- Yandex Disk API

---

## ⚙️ Установка и запуск

### 1. Клонирование репозитория

```bash
git clone <URL_репозитория>
cd yacut
```

### 2. Создание виртуального окружения

Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:
```bash
python -m venv venv
source venv/Scripts/activate
```

---

### 3. Установка зависимостей

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4. Настройка окружения

Создайте файл `.env` на основе `.env.example`:

```env
FLASK_APP=yacut
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URI=sqlite:///db.sqlite3

YADISK_API_HOST=https://cloud-api.yandex.net/
YADISK_API_VERSION=v1
DISK_TOKEN=your_token_here
```

---

### 5. Миграции БД

```bash
flask db upgrade
```

---

### 6. Запуск

```bash
flask run
```
Приложение будет доступно:

```bash
http://127.0.0.1:5000/
```
---

## 📡 REST API

### Создать короткую ссылку

POST `/api/v1/id/`

```json
{
  "url": "https://example.com/very/long/path",
  "custom_id": "myshort"
}
```

Ответ:

```json
{
  "url": "https://example.com/very/long/path",
  "short_link": "http://127.0.0.1:5000/myshort"
}
```

### Получить оригинальную ссылку

GET `/api/v1/id/<short_id>/`

Ответ:

```json
{
  "url": "https://example.com/very/long/path"
}
```

---

## 📁 Функциональность файлов

- Загрузка файлов через веб-интерфейс: `/files`
- Асинхронная отправка на Яндекс.Диск
- Генерация коротких ссылок для файлов

---

## 🧠 Особенности реализации

- Factory pattern для Flask приложения
- Асинхронная загрузка файлов через asyncio + aiohttp
- Проверка уникальности short_id через SQL-запросы
- Разделение логики на services / views / api
- CSRF защита для форм
- Централизованные обработчики ошибок

---

## 🗂 Структура проекта
```
async-yacut/
├── yacut/
│   ├── services/
│   │   ├── shortener.py      # Логика генерации уникальных short_id
│   │   └── yadisk.py         # Константы и утилиты для Yandex Disk API
│   ├── static/
│   │   ├── css/
│   │   ├── img/
│   │   └── js/
│   ├── templates/
│   │   ├── errors/
│   │   │   ├── 404.html      # Страница ошибки 404
│   │   │   └── 500.html      # Страница ошибки 500
│   │   ├── base.html         # Базовый шаблон с подключением статики
│   │   ├── files.html        # Страница загрузки файлов
│   │   └── index.html        # Главная страница (форма сокращения)
│   ├── __init__.py           # Factory function create_app()
│   ├── api_views.py          # Эндпоинты REST API (/api/id/)
│   ├── config.py             # Конфигурация приложения и загрузка переменных окружения
│   ├── error_handlers.py     # Глобальные обработчики ошибок 404/500
│   ├── extensions.py         # Инициализация расширений (db, migrate, csrf)
│   ├── forms.py              # Flask-WTF формы (ShortenForm, UploadForm)
│   ├── models.py             # SQLAlchemy модели (URLMap)
│   └── views.py              # View-функции для веб-интерфейса
├── .env.example              # Шаблон переменных окружения
├── README.md                 # Описание проекта
└── requirements.txt          # Зависимости проекта
```
