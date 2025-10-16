import requests
import json
from typing import Dict

API_BASE_URL = "http://localhost:8000"

def test_search():
    print("\n=== Тест 1: Поиск ответа ===")
    response = requests.post(
        f"{API_BASE_URL}/api/search",
        json={
            "query": "Как стать клиентом банка онлайн?",
            "top_k": 3
        }
    )
    print(f"Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Draft ответ: {data.get('draft', 'N/A')[:100]}...")
        print(f"Альтернатив: {len(data.get('alternatives', []))}")
        print(f"Источников: {len(data.get('results_meta', []))}")
    else:
        print(f"Ошибка: {response.text}")

def test_feedback():
    print("\n=== Тест 2: Отправка feedback ===")
    response = requests.post(
        f"{API_BASE_URL}/api/feedback",
        json={
            "original_question": "Как стать клиентом банка онлайн?",
            "original_answer": "Стать клиентом можно онлайн через сайт или приложение",
            "edited_answer": "Онлайн-регистрация временно недоступна. Используйте отделение банка.",
            "note": "Тестовая правка"
        }
    )
    print(f"Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Internal token: {data.get('internal_token', 'N/A')}")
    else:
        print(f"Ошибка: {response.text}")

def test_add_qa():
    print("\n=== Тест 3: Добавление новой Q&A ===")
    response = requests.post(
        f"{API_BASE_URL}/api/qa/add",
        json={
            "question": "Как сменить временный пароль при первом входе?",
            "answer": "После первого входа замените временный пароль на постоянный в настройках.",
            "taxonomy": {
                "category": "Новые клиенты",
                "subcategory": "Первые шаги",
                "subtopic": "Первый вход"
            }
        }
    )
    print(f"Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Статус: {data.get('status', 'N/A')}")
    else:
        print(f"Ошибка: {response.text}")

def test_pending():
    print("\n=== Тест 4: Получение pending правок ===")
    response = requests.get(f"{API_BASE_URL}/api/moderation/pending")
    print(f"Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        items = data.get('items', [])
        print(f"Правок в очереди: {len(items)}")
        if items:
            print(f"\nПервая правка:")
            item = items[0]
            print(f"  Token: {item.get('internal_token', 'N/A')[:8]}...")
            print(f"  Вопрос: {item.get('original_question', 'N/A')[:50]}...")
            print(f"  Оператор: {item.get('suggested_by', 'N/A')}")
    else:
        print(f"Ошибка: {response.text}")

def test_resolve():
    print("\n=== Тест 5: Разрешение правки (пропущен, нужен real token) ===")
    print("Используйте token из теста 2 или 4")

def test_stats():
    print("\n=== Тест 6: Статистика ===")
    response = requests.get(f"{API_BASE_URL}/api/moderation/stats")
    print(f"Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Pending: {data.get('total_pending', 0)}")
        print(f"Approved: {data.get('total_approved', 0)}")
        print(f"Rejected: {data.get('total_rejected', 0)}")
    else:
        print(f"Ошибка: {response.text}")

if __name__ == "__main__":
    print("=" * 60)
    print("Тестирование RAG Support API")
    print("=" * 60)
    
    try:
        test_search()
        test_feedback()
        test_add_qa()
        test_pending()
        test_resolve()
        test_stats()
        
        print("\n" + "=" * 60)
        print("Тестирование завершено!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Ошибка: Backend API недоступен на http://localhost:8000")
        print("Убедитесь, что backend запущен перед тестированием.")
    except Exception as e:
        print(f"\n❌ Ошибка: {str(e)}")

