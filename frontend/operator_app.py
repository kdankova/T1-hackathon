import streamlit as st
import requests
import json
from config import API_BASE_URL, API_TIMEOUT

st.set_page_config(
    page_title="RAG Support - Operator",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 RAG Support - Operator Panel")

def search_api(query, top_k=3):
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/search",
            json={"query": query, "top_k": top_k},
            timeout=API_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Ошибка API: {str(e)}")
        return None

def send_feedback(original_question, original_answer, edited_answer, note):
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/feedback",
            json={
                "original_question": original_question,
                "original_answer": original_answer,
                "edited_answer": edited_answer,
                "note": note
            },
            timeout=API_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Ошибка отправки feedback: {str(e)}")
        return None

col1, col2 = st.columns([2, 1])

with col1:
    st.header("🔍 Поиск в базе знаний")
    
    query = st.text_input("Введите вопрос клиента:", placeholder="Например: как получить кредит?")
    
    if st.button("Поиск", type="primary"):
        if query:
            with st.spinner("Поиск в базе знаний..."):
                result = search_api(query)
                
                if result:
                    st.success("✅ Найден ответ!")
                    
                    st.subheader("📝 Предложенный ответ:")
                    st.write(result["draft"])
                    
                    st.subheader("📚 Альтернативные варианты:")
                    for i, alt in enumerate(result["alternatives"], 1):
                        st.write(f"{i}. {alt}")
                    
                    st.subheader("📋 Метаданные:")
                    for i, meta in enumerate(result["results_meta"], 1):
                        with st.expander(f"Результат {i}: {meta['question']}"):
                            st.write(f"**Категория:** {meta['taxonomy']['category']}")
                            st.write(f"**Подкатегория:** {meta['taxonomy']['subcategory']}")
                            st.write(f"**Ответ:** {meta['answer']}")

with col2:
    st.header("ℹ️ Информация")
    st.info("""
    **Как использовать:**
    1. Введите вопрос клиента
    2. Нажмите "Поиск"
    3. Используйте найденный ответ для помощи клиенту
    4. Просмотрите альтернативные варианты при необходимости
    """)
    
    st.header("🔗 API статус")
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        if response.status_code == 200:
            st.success("✅ API работает")
        else:
            st.error("❌ API недоступен")
    except:
        st.error("❌ API недоступен")

