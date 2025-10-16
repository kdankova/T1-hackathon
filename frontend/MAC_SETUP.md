# Установка на Mac (Arc браузер)

## 🍎 Специально для macOS + Arc

### Горячие клавиши на Mac

**Важно!** На Mac используйте `Cmd` вместо `Ctrl`:

| Действие | Горячие клавиши |
|----------|----------------|
| Скрыть/показать панель | `Cmd + Shift + K` |
| Копировать ответ | `Cmd + Enter` |
| Очистить форму | `Esc` |

### Быстрый старт (5 минут)

#### 1. Установка зависимостей

Откройте Terminal.app и выполните:

```bash
cd /Users/kdankova/EDU/hack-rag/T1-hackathon/frontend
pip install -r requirements.txt
```

#### 2. Запуск Streamlit интерфейсов

Откройте **2 вкладки** в Terminal:

**Вкладка 1 - Оператор:**
```bash
cd /Users/kdankova/EDU/hack-rag/T1-hackathon/frontend
streamlit run operator_app.py
```

**Вкладка 2 - Модератор:**
```bash
cd /Users/kdankova/EDU/hack-rag/T1-hackathon/frontend
streamlit run moderator_app.py --server.port 8502
```

#### 3. Открытие в Arc

В Arc браузере откройте:
- http://localhost:8501 (оператор)
- http://localhost:8502 (модератор)

✅ **Готово!** Можете работать с обоими интерфейсами одновременно в разных вкладках/окнах.

---

## 📌 Bookmarklet в Arc (опционально)

Если хотите встроить панель на любой сайт:

### Шаг 1: Запустите embed сервер

```bash
cd /Users/kdankova/EDU/hack-rag/T1-hackathon/frontend
python3 -m http.server 8080
```

### Шаг 2: Создайте bookmarklet в Arc

1. Откройте любую страницу в Arc
2. Нажмите `Cmd + D` (добавить в закладки)
3. В открывшемся окне:
   - **Name:** RAG Support
   - **URL:** вставьте код ниже целиком

```javascript
javascript:(function(){var s=document.createElement('script');s.src='http://localhost:8080/embed.js';document.body.appendChild(s);})();
```

4. Нажмите "Save"

### Шаг 3: Тест

1. Откройте тестовую страницу: http://localhost:8080/test_bookmarklet.html
2. Или откройте любой сайт (например, gmail.com)
3. Выделите какой-нибудь текст (необязательно)
4. Нажмите на закладку "RAG Support" в Arc
5. Справа должна появиться панель!

### Шаг 4: Используйте горячие клавиши

- `Cmd + Shift + K` - скрыть/показать панель
- `Cmd + Enter` - копировать ответ
- `Esc` - очистить форму

---

## 🎯 Два режима работы

### Режим 1: Streamlit (основной)

**Использование:**
- Открываете http://localhost:8501 в Arc
- Работаете как с обычным веб-приложением
- Можно открыть несколько вкладок/окон одновременно

**Когда использовать:**
- Основная работа операторов
- Модерация (только в Streamlit!)
- Просмотр статистики

### Режим 2: Bookmarklet (встраиваемая панель)

**Использование:**
- Открываете любой сайт (CRM, тикет-систему, etc)
- Нажимаете bookmarklet
- Справа появляется RAG панель
- Не нужно переключаться между вкладками!

**Когда использовать:**
- Интеграция в существующие системы
- Быстрый доступ к RAG без переключения вкладок
- Работа в нескольких системах одновременно

---

## 🔧 Arc-специфичные настройки

### Если горячие клавиши не работают

Arc имеет собственные горячие клавиши, которые могут конфликтовать:

1. Откройте Arc Settings: `Cmd + ,`
2. Перейдите в **Shortcuts**
3. Проверьте что `Cmd + Shift + K` не занят

Альтернатива - измените горячие клавиши в `embed.js`:

```javascript
// Вместо 'k' используйте другую букву, например 'r'
if (modKey && e.shiftKey && e.key.toLowerCase() === 'r') {
```

### Split View в Arc

Arc поддерживает Split View - идеально для одновременной работы:

1. Откройте http://localhost:8501 (оператор)
2. Нажмите `Cmd + Shift + D` в Arc
3. В второй панели откройте http://localhost:8502 (модератор)

Теперь видите оба интерфейса одновременно! 🎉

### Spaces в Arc

Создайте отдельный Space для RAG Support:

1. Создайте новый Space: `Cmd + T` → "New Space"
2. Назовите "RAG Support"
3. Добавьте вкладки:
   - http://localhost:8501 (оператор)
   - http://localhost:8502 (модератор)
4. Закрепите их: правый клик → "Pin"

Быстрое переключение между Spaces: `Cmd + [` / `Cmd + ]`

---

## 🐛 Траблшутинг на Mac

### Порт занят

Если порт 8501/8502 занят:

```bash
# Найти процесс
lsof -i :8501

# Убить процесс
kill -9 <PID>

# Или используйте другой порт
streamlit run operator_app.py --server.port 8503
```

### Python не найден

```bash
# Установите Python через Homebrew
brew install python3

# Или используйте python3 явно
python3 -m pip install -r requirements.txt
```

### Permission denied при установке

```bash
# Используйте виртуальное окружение
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Streamlit не запускается

```bash
# Обновите pip
pip install --upgrade pip

# Переустановите streamlit
pip install --force-reinstall streamlit
```

---

## 💡 Советы для продуктивности в Arc

1. **Используйте Command Bar:** `Cmd + T` → набирайте "8501" для быстрого открытия
2. **Закрепите вкладки:** Правый клик → "Pin" чтобы вкладки всегда были наверху
3. **Mini player:** В Arc можно открыть панель в маленьком окне поверх других приложений
4. **Split View:** `Cmd + Shift + D` для одновременного просмотра оператора и модератора
5. **Picture-in-Picture:** Если нужно видеть интерфейс поверх других окон

---

## 📚 Дополнительные ресурсы

- `ABOUT_MODES.md` - подробно про режимы работы
- `QUICKSTART.md` - быстрый старт
- `BOOKMARKLET.md` - детали про bookmarklet
- `test_bookmarklet.html` - страница для тестирования

---

## ✅ Чеклист готовности

- [ ] Python установлен: `python3 --version`
- [ ] Зависимости установлены: `pip list | grep streamlit`
- [ ] Backend запущен на порту 8000: `curl http://localhost:8000/health`
- [ ] Streamlit оператор работает: http://localhost:8501
- [ ] Streamlit модератор работает: http://localhost:8502
- [ ] (Опционально) Embed сервер запущен: http://localhost:8080/test_bookmarklet.html
- [ ] (Опционально) Bookmarklet создан в Arc
- [ ] (Опционально) Горячие клавиши работают: `Cmd + Shift + K`

Если все пункты отмечены - готово к работе! 🚀

