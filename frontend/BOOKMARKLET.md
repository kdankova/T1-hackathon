# Встраиваемая сайд-панель (Bookmarklet)

## Что это?

Bookmarklet позволяет встроить RAG Support панель на любую веб-страницу одним кликом.

## Установка bookmarklet

### Способ 1: Перетаскивание

1. Откройте эту страницу в браузере
2. Создайте новую закладку и вставьте в URL:

```javascript
javascript:(function(){var s=document.createElement('script');s.src='http://localhost:8080/embed.js';document.body.appendChild(s);})();
```

3. Сохраните закладку с именем "RAG Support"

### Способ 2: Ручное создание

1. Создайте новую закладку в браузере
2. Назовите её "RAG Support" 
3. В поле URL вставьте код выше
4. Сохраните

## Использование

1. Откройте любую веб-страницу (например, CRM или тикет-систему)
2. Выделите текст вопроса клиента (опционально)
3. Нажмите на закладку "RAG Support"
4. Справа появится панель с интерфейсом оператора

## Горячие клавиши

**macOS:**
- `Cmd+Shift+K` - скрыть/показать панель
- `Cmd+Enter` - копировать ответ
- `Esc` - очистить форму

**Windows/Linux:**
- `Ctrl+Shift+K` - скрыть/показать панель
- `Ctrl+Enter` - копировать ответ
- `Esc` - очистить форму

## Настройка для production

Измените URL в bookmarklet на ваш production адрес:

```javascript
javascript:(function(){var s=document.createElement('script');s.src='https://ваш-домен.com/embed.js';document.body.appendChild(s);})();
```

## Запуск embed сервера

Для локальной разработки запустите простой HTTP сервер:

```bash
cd frontend
python -m http.server 8080
```

Затем embed.html будет доступен по адресу: http://localhost:8080/embed.html

## Интеграция в iframe

Вы также можете встроить панель напрямую в iframe:

```html
<iframe 
  src="http://localhost:8080/embed.html" 
  style="position:fixed; top:0; right:0; width:420px; height:100vh; border:none; z-index:9999;"
></iframe>
```

## Безопасность

При использовании в production:

1. Используйте HTTPS
2. Настройте CORS на backend
3. Добавьте аутентификацию
4. Ограничьте источники iframe (Content-Security-Policy)

## Ограничения

- Работает только если backend API доступен с той же страницы (или CORS настроен)
- Некоторые сайты могут блокировать встраивание через Content-Security-Policy
- Bookmarklet может не работать на страницах с strict CSP

## Альтернатива: Браузерное расширение

Для более надёжной интеграции рекомендуется создать браузерное расширение (Chrome Extension / Firefox Add-on).

