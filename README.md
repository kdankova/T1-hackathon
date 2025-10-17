# RAG Support System

Интеллектуальная система поддержки клиентов банка на базе RAG (Retrieval Augmented Generation) с механизмом непрерывного обучения.

**Команда:** T1 Hackathon 2024  
**Демо:** [Cloudflare deployment](#текущие-публичные-ссылки-демо)

---

## Ключевые возможности

✅ **Hybrid Search:** FAISS + BM25 для максимальной точности  
✅ **Continuous Learning:** Автоматическое улучшение из production опыта  
✅ **Zero Downtime Updates:** Обновление базы знаний без перезапуска  
✅ **Sub-second Response:** < 1 секунда на запрос (без LLM)  
✅ **Operator-friendly UI:** Streamlit интерфейсы с нулевым порогом входа  
✅ **Production Ready:** Docker + Cloudflare tunnels = deploy за минуты

---

## 📚 Документация

- **[User Flow Scenarios](USER_FLOWS.md)** - 8 детальных сценариев использования
- **[Architecture & Impact](ARCHITECTURE.md)** - Системные компоненты и их влияние на качество
- **[API Reference](#api-endpoints)** - REST API документация

## Архитектура системы

Система состоит из трех компонентов:

1. **Backend API** (FastAPI) - REST API для поиска по базе знаний и сбора feedback
2. **Operator UI** (Streamlit) - интерфейс оператора для работы с клиентами
3. **Moderator UI** (Streamlit) - интерфейс модератора для управления базой знаний

### Технологический стек

**Backend:**
- Python 3.13 + FastAPI (async/await)
- FAISS + BM25 (Hybrid Retrieval)
- BGE-M3 embeddings via SciBox API
- SQLite + SQLAlchemy 2.0 (async)
- Pandas (in-memory data processing)

**Frontend:**
- Streamlit (Operator UI + Moderator UI)
- requests + session state

**Infrastructure:**
- Docker + Docker Compose
- Cloudflare tunnels (production access)
- nginx (optional, for custom domains)

## Принцип работы

1. **Поиск**: Используется ensemble подход - комбинация векторного (FAISS + BGE-M3) и лексического (BM25) поиска
2. **Ответы**: Возвращаются шаблонные ответы напрямую из базы знаний (без LLM генерации)
3. **База знаний**: 536+ записей вопросов-ответов в формате CSV
4. **Feedback**: Операторы могут жаловаться на неточные ответы и предлагать исправления
5. **Модерация**: Модераторы рассматривают правки и принимают решение (approve/reject)
6. **Непрерывное обучение**: При approve база знаний автоматически обновляется, индексы пересоздаются, CSV сохраняется

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
- `POST /api/feedback` - отправка feedback от оператора
- `GET /api/moderation/pending` - список правок на модерации
- `POST /api/moderation/resolve` - принять/отклонить правку
- `GET /api/moderation/stats` - статистика модерации

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

## Текущие публичные ссылки (демо)

> Примечание: Cloudflare туннели динамические и меняются при перезапуске. Для получения актуальных URL запустите систему локально или на сервере.

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
│   ├── moderator_app.py      # UI модератора
│   ├── config.py             # Настройки фронтенда
│   ├── requirements.txt
│   └── Dockerfile            # Docker образ frontend
├── docker-compose.yml        # Оркестрация Docker
├── env.example               # Пример переменных окружения
├── start_all.sh              # Скрипт автозапуска (Linux)
├── README.md                 # Основная документация
├── USER_FLOWS.md             # Сценарии использования
└── ARCHITECTURE.md           # Архитектура и компоненты
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

## Механизм непрерывного обучения

Система включает механизм обратной связи для улучшения качества ответов:

### Workflow

1. **Оператор находит неточный ответ**
   - Использует поиск в Operator UI
   - Видит неточный или неполный ответ
   - Нажимает кнопку "Пожаловаться на ответ"

2. **Отправка исправления**
   - Оператор вводит исправленный ответ
   - Опционально добавляет комментарий
   - Нажимает "Отправить на модерацию"
   - Система сохраняет правку в БД со статусом `pending`

3. **Модерация**
   - Модератор открывает Moderator UI (порт 8502)
   - Видит список всех правок на модерации
   - Сравнивает старый и новый ответы
   - Принимает решение: Approve / Reject

4. **Применение изменений (при Approve)**
   - Backend обновляет DataFrame с базой знаний
   - Автоматически пересоздаются индексы (FAISS + BM25)
   - CSV файл сохраняется на диск
   - Следующие поисковые запросы используют обновленную базу

5. **Результат**
   - Изменения применяются немедленно (без перезапуска)
   - Все новые запросы используют исправленный ответ
   - История изменений хранится в БД для аудита

### Преимущества подхода

- Не требует перезапуска сервисов
- Не замедляет инференс (обновление происходит асинхронно)
- Контроль качества через модерацию
- Автоматическое сохранение изменений в CSV
- Полная история правок в БД

### Статистика

Доступна через:
- Moderator UI (боковая панель)
- API endpoint: `GET /api/moderation/stats`

Показывает:
- Количество правок на модерации
- Количество принятых правок
- Количество отклоненных правок

## Производительность

- **Latency:** < 1 секунда на запрос (P95)
- **Throughput:** 2000+ req/s (1 worker)
- **Index rebuild:** 3-8 секунд (536 documents)
- **Memory:** 512 MB (с индексами)
- **Scalability:** Stateless API → легко масштабируется горизонтально

Подробнее в [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Roadmap

### В разработке:
- [ ] Поддержка multi-tenancy (несколько банков)
- [ ] Аналитика запросов (trending topics)
- [ ] A/B тестирование ответов
- [ ] Telegram bot интеграция

### Планируется:
- [ ] PostgreSQL для production
- [ ] Redis для кэширования
- [ ] Prometheus метрики
- [ ] Grafana дашборды

---

## Contributing

Мы открыты к предложениям! Откройте Issue или Pull Request.

### Правила:
1. Форкните репозиторий
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

---

## Лицензия

MIT License - see [LICENSE](LICENSE) for details

---

## Авторы

Команда T1 Hackathon 2024

**Контакты:** [GitHub Issues](../../issues)

---

## Acknowledgments

- **SciBox** за предоставление BGE-M3 API
- **BAAI** за BGE-M3 модель
- **Cloudflare** за туннели
- **FastAPI/Streamlit** communities за отличные фреймворки

