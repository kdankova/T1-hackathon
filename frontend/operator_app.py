import streamlit as st
import requests
import json
from datetime import datetime
from typing import Optional, Dict, List

API_BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="RAG Support - Оператор",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .draft-answer {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .meta-info {
        background-color: #e8eaf6;
        padding: 0.5rem;
        border-radius: 0.3rem;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
    }
    .alternative-answer {
        background-color: #fff3cd;
        padding: 0.8rem;
        border-radius: 0.3rem;
        margin: 0.5rem 0;
        border-left: 3px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

if 'draft_answer' not in st.session_state:
    st.session_state.draft_answer = ""
if 'original_answer' not in st.session_state:
    st.session_state.original_answer = ""
if 'current_question' not in st.session_state:
    st.session_state.current_question = ""
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'internal_token' not in st.session_state:
    st.session_state.internal_token = None

def search_answer(query: str, top_k: int = 3) -> Optional[Dict]:
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/search",
            json={"query": query, "top_k": top_k},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Ошибка API: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка подключения к API: {str(e)}")
        return None

def send_feedback(original_question: str, original_answer: str, edited_answer: str, note: str = "") -> bool:
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/feedback",
            json={
                "original_question": original_question,
                "original_answer": original_answer,
                "edited_answer": edited_answer,
                "note": note
            },
            timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            st.session_state.internal_token = result.get('internal_token')
            return True
        else:
            st.error(f"Ошибка отправки feedback: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка подключения к API: {str(e)}")
        return False

def add_new_qa(question: str, answer: str, category: str, subcategory: str, subtopic: str) -> bool:
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/qa/add",
            json={
                "question": question,
                "answer": answer,
                "taxonomy": {
                    "category": category,
                    "subcategory": subcategory,
                    "subtopic": subtopic
                }
            },
            timeout=10
        )
        if response.status_code == 200:
            return True
        else:
            st.error(f"Ошибка добавления Q&A: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка подключения к API: {str(e)}")
        return False

st.markdown('<div class="main-header">🎯 RAG Support - Панель оператора</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Запрос клиента")
    question = st.text_area(
        "Вопрос клиента",
        value=st.session_state.current_question,
        height=100,
        placeholder="Вставьте или введите вопрос клиента здесь...",
        label_visibility="collapsed"
    )
    
    col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])
    with col_btn1:
        search_btn = st.button("🔍 Найти ответ", type="primary", use_container_width=True)
    with col_btn2:
        clear_btn = st.button("🗑️ Очистить", use_container_width=True)

    if search_btn and question:
        with st.spinner("Поиск ответа..."):
            results = search_answer(question)
            if results:
                st.session_state.search_results = results
                st.session_state.draft_answer = results.get('draft', '')
                st.session_state.original_answer = results.get('draft', '')
                st.session_state.current_question = question
                st.rerun()
    
    if clear_btn:
        st.session_state.draft_answer = ""
        st.session_state.original_answer = ""
        st.session_state.current_question = ""
        st.session_state.search_results = None
        st.session_state.internal_token = None
        st.rerun()

    if st.session_state.search_results:
        st.markdown("---")
        st.subheader("Ответ для клиента")
        
        edited_answer = st.text_area(
            "Редактируемый ответ",
            value=st.session_state.draft_answer,
            height=200,
            key="answer_editor",
            label_visibility="collapsed"
        )
        
        col_act1, col_act2, col_act3 = st.columns(3)
        
        with col_act1:
            if st.button("🔄 Вернуть оригинал", use_container_width=True):
                st.session_state.draft_answer = st.session_state.original_answer
                st.rerun()
        
        with col_act2:
            if st.button("📋 Копировать", use_container_width=True):
                st.code(edited_answer, language=None)
                st.success("Текст готов к копированию выше")
        
        with col_act3:
            if st.button("📤 Отправить feedback", use_container_width=True):
                if edited_answer != st.session_state.original_answer:
                    note = st.text_input("Комментарий к правке (опционально)", key="feedback_note")
                    if send_feedback(
                        st.session_state.current_question,
                        st.session_state.original_answer,
                        edited_answer,
                        note
                    ):
                        st.success("✅ Feedback отправлен на модерацию")
                        if st.session_state.internal_token:
                            st.info(f"ID правки: {st.session_state.internal_token[:8]}...")
                else:
                    st.info("Ответ не изменён, feedback не требуется")
        
        if st.session_state.search_results.get('alternatives'):
            with st.expander("📚 Альтернативные формулировки"):
                for i, alt in enumerate(st.session_state.search_results['alternatives'], 1):
                    st.markdown(f'<div class="alternative-answer"><strong>Вариант {i}:</strong><br>{alt}</div>', 
                              unsafe_allow_html=True)

with col2:
    st.subheader("Метаданные")
    
    if st.session_state.search_results and st.session_state.search_results.get('results_meta'):
        for idx, meta in enumerate(st.session_state.search_results['results_meta'], 1):
            with st.expander(f"Источник {idx}", expanded=(idx == 1)):
                taxonomy = meta.get('taxonomy', {})
                st.markdown(f"**Категория:** {taxonomy.get('category', 'N/A')}")
                st.markdown(f"**Подкатегория:** {taxonomy.get('subcategory', 'N/A')}")
                st.markdown(f"**Топик:** {taxonomy.get('subtopic', 'N/A')}")
                
                if 'updated_at' in meta:
                    st.markdown(f"**Обновлено:** {meta['updated_at'][:10]}")
                
                if 'question' in meta:
                    st.markdown(f"**Исходный вопрос:**")
                    st.caption(meta['question'])
    else:
        st.info("Выполните поиск для просмотра метаданных")

st.markdown("---")
st.subheader("➕ Добавить новую пару Q&A")

with st.expander("Добавить новый вопрос-ответ в базу"):
    new_question = st.text_area("Новый вопрос", height=80, key="new_q")
    new_answer = st.text_area("Новый ответ", height=120, key="new_a")
    
    col_tax1, col_tax2, col_tax3 = st.columns(3)
    with col_tax1:
        new_category = st.text_input("Категория", key="new_cat")
    with col_tax2:
        new_subcategory = st.text_input("Подкатегория", key="new_subcat")
    with col_tax3:
        new_subtopic = st.text_input("Топик", key="new_topic")
    
    if st.button("➕ Добавить в базу", type="primary"):
        if new_question and new_answer and new_category:
            if add_new_qa(new_question, new_answer, new_category, new_subcategory, new_subtopic):
                st.success("✅ Новая пара Q&A добавлена и отправлена на модерацию")
                st.balloons()
        else:
            st.warning("Заполните минимум вопрос, ответ и категорию")

st.sidebar.markdown("### ℹ️ Горячие клавиши")
st.sidebar.markdown("""
**Streamlit режим:**
- `R` - обновить интерфейс
- `C` - очистить кэш

**Embed панель (bookmarklet):**
- `Cmd+Shift+K` (Mac) / `Ctrl+Shift+K` (Win) - скрыть/показать
- `Cmd+Enter` (Mac) / `Ctrl+Enter` (Win) - копировать
- `Esc` - очистить форму
""")

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Статус API:** {'🟢 Доступен' if True else '🔴 Недоступен'}")
st.sidebar.markdown(f"**Время:** {datetime.now().strftime('%H:%M:%S')}")

