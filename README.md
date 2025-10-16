# RAG система для банка ВТБ (Беларусь)

Система для автоматического ответа на вопросы клиентов банка с использованием RAG (Retrieval Augmented Generation).

## Архитектура системы

Система состоит из двух компонентов:

1. **Backend API** (FastAPI) - REST API для поиска по базе знаний и сбора feedback
2. **Operator UI** (Streamlit) - интерфейс оператора для работы с клиентами

### Технологический стек

- **Python 3.13**
- **FastAPI** - для REST API
- **Streamlit** - для UI интерфейсов
- **FAISS** - векторный поиск
- **BM25** - лексический поиск
- **Ensemble Retriever** - комбинированный поиск (FAISS + BM25)
- **BGE-M3** - эмбеддинги через SciBox API
- **SQLite** - хранение feedback и очереди модерации
- **Cloudflared** - туннели для публичного доступа

## Принцип работы

1. **Поиск**: Используется ensemble подход - комбинация векторного (FAISS + BGE-M3) и лексического (BM25) поиска
2. **Ответы**: Возвращаются шаблонные ответы напрямую из базы знаний (без LLM генерации)
3. **База знаний**: 536 записей вопросов-ответов в формате CSV
4. **Feedback**: Операторы могут оставлять отзывы о качестве ответов

## Установка и запуск локально

### Требования

**Для Docker (рекомендуется):**
- Docker
- Docker Compose

**Для запуска без Docker:**
- Python 3.13+
- pip

---

## Вариант 1: Docker Compose (Рекомендуется)

### 1. Клонировать репозиторий

```bash
git clone <repository-url>
cd T1-hackathon
```

### 2. Настроить переменные окружения

Создайте файл `.env` в корне проекта:

```bash
cp env.example .env
```

Отредактируйте `.env` и укажите ваш API ключ от SciBox:

```env
API_KEY=your_scibox_api_key_here
```

### 3. Запустить все сервисы

```bash
docker-compose up -d
```

### 4. Проверить работу

- Backend API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- Operator UI: http://localhost:8501

### 5. Просмотр логов

```bash
# Все сервисы
docker-compose logs -f

# Только backend
docker-compose logs -f backend

# Только frontend
docker-compose logs -f frontend
```

### 6. Остановить сервисы

```bash
docker-compose down
```

---

## Вариант 2: Запуск без Docker

### 1. Клонировать репозиторий

```bash
git clone <repository-url>
cd T1-hackathon
```

### 2. Установить зависимости

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
pip install -r requirements.txt
```

### 3. Настроить переменные окружения

Создайте файл `backend/.env`:

```env
API_KEY=your_scibox_api_key
LLM_BASE_URL=https://llm.t1v.scibox.tech/v1
LLM_MODEL=Qwen2.5-72B-Instruct-AWQ
DATABASE_URL=sqlite+aiosqlite:///./data/feedback.db
```

### 4. Подготовить данные

Убедитесь что файл `backend/data/knowledge_base_augmented2.csv` на месте.

### 5. Запустить сервисы

#### Вручную в разных терминалах

**Терминал 1 - Backend:**
```bash
cd backend
python3.13 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Терминал 2 - Operator UI:**
```bash
cd frontend
python3.13 -m streamlit run operator_app.py --server.port=8501
```

#### Автоматический запуск (только на сервере Linux)

```bash
bash start_all.sh
```

### 6. Проверить работу

- Backend API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- Operator UI: http://localhost:8501

## API Endpoints

### Основные эндпоинты

- `GET /` - healthcheck
- `POST /api/search` - поиск по базе знаний
- `POST /api/feedback` - отправка feedback
- `GET /api/stats` - статистика системы

### Пример запроса

```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Как оформить карту MORE?",
    "top_k": 3
  }'
```

## Swagger документация

Полная интерактивная документация API доступна по адресу:

**Локально:** http://localhost:8000/docs  
**На сервере:** https://begins-mrna-safe-effectively.trycloudflare.com/docs

## Текущие публичные ссылки (демо)

- **Backend API:** https://begins-mrna-safe-effectively.trycloudflare.com
- **Operator UI:** https://highland-southeast-theory-putting.trycloudflare.com

> Примечание: Cloudflared туннели могут меняться при перезапуске. Для получения актуальных URL используйте команду на сервере.

## Структура проекта

```
T1-hackathon/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI приложение
│   │   ├── rag_service.py    # RAG логика
│   │   ├── embeddings.py     # BGE-M3 эмбеддинги
│   │   ├── database.py       # SQLAlchemy модели
│   │   ├── models.py         # Pydantic схемы
│   │   └── config.py         # Конфигурация
│   ├── data/
│   │   └── knowledge_base_augmented2.csv  # База знаний
│   ├── requirements.txt
│   └── Dockerfile            # Docker образ backend
├── frontend/
│   ├── operator_app.py       # UI оператора
│   ├── config.py             # Настройки фронтенда
│   ├── requirements.txt
│   └── Dockerfile            # Docker образ frontend
├── docker-compose.yml        # Оркестрация Docker
├── env.example               # Пример переменных окружения
├── start_all.sh              # Скрипт автозапуска (Linux)
└── README.md
```

## Использование SciBox API

Система использует только SciBox API:
- **BGE-M3** - для генерации эмбеддингов текста
- Endpoint: `https://llm.t1v.scibox.tech/v1/embeddings`

LLM генерация **не используется** - ответы возвращаются напрямую из базы знаний.

## Управление на сервере

### Запуск всех сервисов

```bash
bash /home/kate/T1-hackathon/start_all.sh
```

### Остановка всех сервисов

```bash
pkill -f "uvicorn\|streamlit\|cloudflared"
```

### Просмотр логов

```bash
tail -f /tmp/backend.log      # Backend
tail -f /tmp/operator.log     # Operator UI
```

### Проверка запущенных процессов

```bash
ps aux | grep -E "(uvicorn|streamlit|cloudflared)" | grep -v grep
```

## Разработка

### Добавление новых вопросов в базу знаний

1. Откройте `backend/data/knowledge_base_augmented2.csv`
2. Добавьте новые строки в формате:
   - Основная категория
   - Подкатегория
   - Пример вопроса
   - Целевая аудитория
   - Шаблонный ответ
   - is_original
3. Перезапустите backend для переиндексации

### Тестирование через Swagger

1. Откройте http://localhost:8000/docs
2. Выберите endpoint (например, `/api/search`)
3. Нажмите "Try it out"
4. Заполните параметры
5. Нажмите "Execute"

## Производительность

- Время ответа: < 1 секунда (без LLM)
- Batch size для эмбеддингов: 64
- Параллельность: 8 workers
- Timeout: 120 секунд

## Лицензия

MIT

## Авторы

Команда T1 Hackathon 2024

