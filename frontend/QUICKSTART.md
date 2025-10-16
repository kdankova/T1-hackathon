# Быстрый старт - RAG Support Frontend

## За 3 минуты

### 1. Установка (30 сек)

```bash
cd frontend
pip install -r requirements.txt
```

### 2. Запуск backend (если ещё не запущен)

```bash
cd ../backend
python app.py
```

Backend должен быть доступен на `http://localhost:8000`

### 3. Запуск интерфейсов (1 мин)

Откройте 2 терминала:

**Терминал 1 - Оператор:**
```bash
cd frontend
streamlit run operator_app.py
```
Откройте: http://localhost:8501

**Терминал 2 - Модератор:**
```bash
cd frontend
streamlit run moderator_app.py --server.port 8502
```
Откройте: http://localhost:8502

### 4. Тестирование (1 мин)

**Как оператор:**

1. Вставьте вопрос: "Как стать клиентом банка онлайн?"
2. Нажмите "🔍 Найти ответ"
3. Отредактируйте ответ
4. Нажмите "📤 Отправить feedback"

**Как модератор:**

1. Откройте вкладку "📋 Очередь правок"
2. Просмотрите правку от оператора
3. Нажмите "✅ Одобрить" или "❌ Отклонить"

## Docker (альтернатива)

```bash
cd frontend
docker-compose up -d
```

Готово! Оба интерфейса запущены.

## Встраиваемая панель (bookmarklet)

1. Запустите embed сервер:
```bash
cd frontend
python -m http.server 8080
```

2. Создайте закладку в браузере с URL:
```javascript
javascript:(function(){var s=document.createElement('script');s.src='http://localhost:8080/embed.js';document.body.appendChild(s);})();
```

3. Откройте любой сайт и нажмите закладку
4. Справа появится панель оператора

## Проверка API

```bash
cd frontend
python test_api.py
```

Этот скрипт протестирует все endpoints backend API.

## Проблемы?

**Backend не отвечает:**
- Убедитесь, что backend запущен на порту 8000
- Проверьте: `curl http://localhost:8000/health`

**Streamlit не запускается:**
- Переустановите: `pip install --upgrade streamlit`
- Проверьте порты: `lsof -i :8501`

**Embed панель не появляется:**
- Откройте консоль браузера (F12)
- Проверьте CORS ошибки
- Убедитесь, что embed сервер запущен

## Что дальше?

Смотрите полную документацию:
- `SETUP.md` - детальная установка и конфигурация
- `BOOKMARKLET.md` - интеграция bookmarklet
- `README.md` - обзор всех компонентов

## Горячие клавиши

**Streamlit (оператор и модератор):**
- `R` - обновить интерфейс
- `C` - очистить кэш Streamlit

**Embed панель (bookmarklet):**

_macOS:_
- `Cmd+Shift+K` - скрыть/показать панель
- `Cmd+Enter` - копировать ответ
- `Esc` - очистить форму

_Windows/Linux:_
- `Ctrl+Shift+K` - скрыть/показать панель
- `Ctrl+Enter` - копировать ответ
- `Esc` - очистить форму

