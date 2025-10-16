# Как запустить на своём компьютере

## Требования
- Docker Desktop (для Windows/Mac) или Docker + Docker Compose (для Linux)
- Git

## Быстрый старт

### 1. Установить Docker
- **Windows/Mac**: Скачай [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Linux**: 
  ```bash
  sudo apt-get update
  sudo apt-get install docker.io docker-compose
  ```

### 2. Клонировать репозиторий
```bash
git clone <url-репозитория>
cd T1-hackathon
```

### 3. Настроить API ключ
```bash
# Создай .env файл из примера
cp env.example .env

# Отредактируй .env и укажи свой API ключ от SciBox
# API_KEY=твой_ключ_здесь
```

### 4. Запустить
```bash
docker-compose up -d
```

### 5. Проверить
Открой в браузере:
- **Swagger API**: http://localhost:8000/docs
- **Operator UI**: http://localhost:8501

## Полезные команды

### Просмотр логов
```bash
# Все сервисы
docker-compose logs -f

# Только backend
docker-compose logs -f backend

# Только frontend
docker-compose logs -f frontend
```

### Проверка статуса
```bash
docker-compose ps
```

### Остановка
```bash
docker-compose down
```

### Перезапуск
```bash
docker-compose restart
```

### Пересборка после изменений
```bash
docker-compose up -d --build
```

### Полная очистка
```bash
docker-compose down -v
```

## Troubleshooting

### Порты заняты
Если порты 8000 или 8501 уже заняты, измени их в `docker-compose.yml`:
```yaml
ports:
  - "8080:8000"  # вместо 8000:8000
  - "8502:8501"  # вместо 8501:8501
```

### Backend не запускается
Проверь что API ключ указан в `.env` файле:
```bash
cat .env | grep API_KEY
```

### Frontend не может подключиться к backend
Убедись что оба контейнера запущены:
```bash
docker-compose ps
```

### Нужно пересобрать образы
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Что внутри

- **Backend** (порт 8000): FastAPI + RAG система
- **Frontend** (порт 8501): Streamlit интерфейс оператора
- **База данных**: SQLite в `backend/data/`
- **База знаний**: CSV файл в `backend/data/knowledge_base_augmented2.csv`

## Проверка работы

1. Открой Swagger: http://localhost:8000/docs
2. Попробуй endpoint `/api/search`:
   ```json
   {
     "query": "Как оформить карту?",
     "top_k": 3
   }
   ```
3. Открой Operator UI: http://localhost:8501
4. Введи вопрос и проверь результат

Готово! 🚀
