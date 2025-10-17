import streamlit as st
import requests
import json
from datetime import datetime
from config import API_BASE_URL, API_TIMEOUT

st.set_page_config(
    page_title="RAG Support - Moderator",
    page_icon="👨‍⚖️",
    layout="wide"
)

st.title("👨‍⚖️ RAG Support - Moderator Panel")

def get_pending_items():
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/moderation/pending",
            timeout=API_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Ошибка получения списка: {str(e)}")
        return None

def resolve_feedback(internal_token, action):
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/moderation/resolve",
            json={
                "internal_token": internal_token,
                "action": action
            },
            timeout=API_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Ошибка обработки: {str(e)}")
        return None

def get_stats():
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/moderation/stats",
            timeout=API_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Ошибка получения статистики: {str(e)}")
        return None

st.sidebar.header("📊 Статистика")
stats = get_stats()
if stats:
    st.sidebar.metric("Ожидает модерации", stats.get("total_pending", 0))
    st.sidebar.metric("Принято", stats.get("total_approved", 0))
    st.sidebar.metric("Отклонено", stats.get("total_rejected", 0))

st.sidebar.divider()

st.sidebar.header("🔗 API статус")
try:
    response = requests.get(f"{API_BASE_URL}/", timeout=5)
    if response.status_code == 200:
        st.sidebar.success("✅ API работает")
    else:
        st.sidebar.error("❌ API недоступен")
except:
    st.sidebar.error("❌ API недоступен")

if st.button("🔄 Обновить список", type="primary"):
    st.rerun()

st.divider()

st.header("📋 Список на модерации")

pending_data = get_pending_items()

if pending_data and pending_data.get("items"):
    items = pending_data["items"]
    st.info(f"Всего правок на модерации: {len(items)}")
    
    for idx, item in enumerate(items, 1):
        with st.expander(f"#{idx} - {item['original_question'][:80]}...", expanded=True):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Токен:** `{item['internal_token']}`")
                st.write(f"**Дата создания:** {item['created_at']}")
                if item.get('suggested_by'):
                    st.write(f"**Предложил:** {item['suggested_by']}")
                
                st.divider()
                
                st.write("**Исходный вопрос:**")
                st.info(item['original_question'])
                
                st.write("**Старый ответ:**")
                st.text_area(
                    "Старый", 
                    value=item['old_answer'], 
                    height=120, 
                    disabled=True,
                    key=f"old_{idx}"
                )
                
                st.write("**Предложенный новый ответ:**")
                st.text_area(
                    "Новый", 
                    value=item['edited_answer'], 
                    height=120, 
                    disabled=True,
                    key=f"new_{idx}"
                )
            
            with col2:
                st.write("")
                st.write("")
                st.write("")
                
                if st.button("✅ Принять", key=f"approve_{idx}", type="primary", use_container_width=True):
                    with st.spinner("Применяю изменения..."):
                        result = resolve_feedback(item['internal_token'], "approve")
                        if result:
                            if result.get("reembedded"):
                                st.success("✅ Изменения применены! База знаний обновлена.")
                            else:
                                st.success("✅ Изменения применены!")
                            st.balloons()
                            st.rerun()
                
                if st.button("❌ Отклонить", key=f"reject_{idx}", use_container_width=True):
                    result = resolve_feedback(item['internal_token'], "reject")
                    if result:
                        st.warning("❌ Правка отклонена")
                        st.rerun()
            
            st.divider()
else:
    st.success("✅ Нет правок на модерации!")
    st.balloons()

