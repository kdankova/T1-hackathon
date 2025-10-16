# 👋 Начните отсюда!

## На Mac? Читайте это!

### Самое главное про горячие клавиши на Mac:

```
❌ НЕ РАБОТАЕТ: Ctrl + Shift + K
✅ РАБОТАЕТ:    Cmd + Shift + K (⌘ + Shift + K)
```

---

## Быстрый запуск за 2 минуты

### Вариант 1: Streamlit (рекомендуется)

**Шаг 1:** Откройте Terminal и выполните:
```bash
cd /Users/kdankova/EDU/hack-rag/T1-hackathon/frontend
pip install -r requirements.txt
streamlit run operator_app.py
```

**Шаг 2:** Откройте в браузере Arc:
http://localhost:8501

**Готово!** 🎉 Работает интерфейс оператора.

---

**Хотите модератора?** Откройте новый Terminal:
```bash
cd /Users/kdankova/EDU/hack-rag/T1-hackathon/frontend
streamlit run moderator_app.py --server.port 8502
```

Откройте: http://localhost:8502

---

### Вариант 2: Bookmarklet (для интеграции в другие сайты)

**Шаг 1:** Запустите сервер:
```bash
cd /Users/kdankova/EDU/hack-rag/T1-hackathon/frontend
python3 -m http.server 8080
```

**Шаг 2:** Откройте тестовую страницу:
http://localhost:8080/test_bookmarklet.html

**Шаг 3:** Следуйте инструкциям на странице.

---

## В чём разница?

| Streamlit | Bookmarklet |
|-----------|-------------|
| Отдельное веб-приложение | Встраивается в любой сайт |
| Полный функционал | Базовый функционал |
| Оператор + Модератор | Только оператор |
| http://localhost:8501 | Работает везде через закладку |

**Для начала используйте Streamlit** - проще и функциональнее!

---

## Можно ли открыть 2 окна одновременно?

**ДА!** В Streamlit режиме:

```
Окно 1: http://localhost:8501 (оператор для клиента A)
Окно 2: http://localhost:8501 (оператор для клиента B)
Окно 3: http://localhost:8502 (модератор)
```

Каждое окно - отдельная сессия!

В Arc можно использовать **Split View** (⌘ + Shift + D) чтобы видеть оба интерфейса одновременно.

---

## Траблшутинг

**Не запускается?**
```bash
# Обновите pip и streamlit
pip install --upgrade pip streamlit
```

**Порт занят?**
```bash
# Найдите что занимает порт
lsof -i :8501

# Убейте процесс или используйте другой порт
streamlit run operator_app.py --server.port 8503
```

**Backend не отвечает?**
Убедитесь что backend API запущен на http://localhost:8000

---

## Что дальше?

После того как запустили Streamlit:

1. **Попробуйте:** Вставьте вопрос → нажмите "🔍 Найти ответ"
2. **Отредактируйте:** Измените текст ответа
3. **Отправьте feedback:** Кнопка "📤 Отправить feedback"
4. **Проверьте модератор:** Откройте http://localhost:8502

---

## Полная документация

- **`MAC_SETUP.md`** ⭐ - специально для Mac и Arc
- **`QUICKSTART.md`** - быстрый старт
- **`ABOUT_MODES.md`** - про режимы работы (Streamlit vs bookmarklet)
- **`BOOKMARKLET.md`** - встраивание через bookmarklet

---

## Нужна помощь?

1. Проверьте `MAC_SETUP.md` - там всё про Mac
2. Откройте `test_bookmarklet.html` для теста bookmarklet
3. Запустите `python test_api.py` для проверки API

**Главное помните:** На Mac используйте `Cmd` вместо `Ctrl`! 🍎

