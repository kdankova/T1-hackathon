import streamlit as st
import requests
import json
from datetime import datetime
from typing import Optional, Dict, List
import difflib

API_BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="RAG Support - Модератор",
    page_icon="👨‍🏫",
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
    .pending-item {
        background-color: #fff9e6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .diff-old {
        background-color: #ffebee;
        padding: 0.5rem;
        border-radius: 0.3rem;
        margin: 0.5rem 0;
    }
    .diff-new {
        background-color: #e8f5e9;
        padding: 0.5rem;
        border-radius: 0.3rem;
        margin: 0.5rem 0;
    }
    .stat-card {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

if 'pending_items' not in st.session_state:
    st.session_state.pending_items = []
if 'selected_item' not in st.session_state:
    st.session_state.selected_item = None
if 'refresh_trigger' not in st.session_state:
    st.session_state.refresh_trigger = 0

def get_pending_items() -> List[Dict]:
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/moderation/pending",
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return data.get('items', [])
        else:
            st.error(f"Ошибка API: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка подключения к API: {str(e)}")
        return []

def resolve_item(internal_token: str, action: str) -> bool:
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/moderation/resolve",
            json={
                "internal_token": internal_token,
                "action": action
            },
            timeout=10
        )
        if response.status_code == 200:
            return True
        else:
            st.error(f"Ошибка разрешения: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка подключения к API: {str(e)}")
        return False

def get_text_diff(old_text: str, new_text: str) -> str:
    old_lines = old_text.splitlines()
    new_lines = new_text.splitlines()
    
    diff = difflib.unified_diff(old_lines, new_lines, lineterm='')
    return '\n'.join(diff)

def get_stats() -> Dict:
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/moderation/stats",
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "total_pending": 0,
                "total_approved": 0,
                "total_rejected": 0,
                "avg_response_time": "N/A"
            }
    except:
        return {
            "total_pending": 0,
            "total_approved": 0,
            "total_rejected": 0,
            "avg_response_time": "N/A"
        }

st.markdown('<div class="main-header">👨‍🏫 RAG Support - Панель модератора</div>', unsafe_allow_html=True)

tabs = st.tabs(["📋 Очередь правок", "📊 Статистика"])

with tabs[0]:
    col_header1, col_header2 = st.columns([4, 1])
    
    with col_header1:
        st.subheader("Правки на модерации")
    
    with col_header2:
        if st.button("🔄 Обновить", use_container_width=True):
            st.session_state.refresh_trigger += 1
            st.rerun()
    
    with st.spinner("Загрузка правок..."):
        pending_items = get_pending_items()
        st.session_state.pending_items = pending_items
    
    if not pending_items:
        st.info("Нет правок на модерации")
    else:
        st.markdown(f"**Всего правок:** {len(pending_items)}")
        
        for idx, item in enumerate(pending_items):
            with st.expander(
                f"ID: {item['internal_token'][:8]}... | {item['original_question'][:60]}...",
                expanded=(idx == 0)
            ):
                st.markdown(f"**Вопрос клиента:**")
                st.info(item['original_question'])
                
                st.markdown("---")
                
                col_diff1, col_diff2 = st.columns(2)
                
                with col_diff1:
                    st.markdown("**Исходный ответ:**")
                    st.markdown(f'<div class="diff-old">{item["old_answer"]}</div>', 
                              unsafe_allow_html=True)
                
                with col_diff2:
                    st.markdown("**Предложенный ответ:**")
                    st.markdown(f'<div class="diff-new">{item["edited_answer"]}</div>', 
                              unsafe_allow_html=True)
                
                st.markdown("---")
                
                col_meta1, col_meta2 = st.columns(2)
                with col_meta1:
                    st.caption(f"**Оператор:** {item.get('suggested_by', 'N/A')}")
                with col_meta2:
                    st.caption(f"**Дата:** {item.get('created_at', 'N/A')[:19]}")
                
                with st.expander("🔍 Текстовый diff"):
                    diff_text = get_text_diff(item['old_answer'], item['edited_answer'])
                    st.code(diff_text, language='diff')
                
                st.markdown("---")
                
                col_action1, col_action2, col_action3 = st.columns([2, 2, 1])
                
                with col_action1:
                    approve_key = f"approve_{item['internal_token']}_{st.session_state.refresh_trigger}"
                    if st.button(
                        "✅ Одобрить и применить",
                        key=approve_key,
                        type="primary",
                        use_container_width=True
                    ):
                        if resolve_item(item['internal_token'], 'approve'):
                            st.success("✅ Правка одобрена и применена к базе")
                            st.balloons()
                            st.session_state.refresh_trigger += 1
                            st.rerun()
                
                with col_action2:
                    reject_key = f"reject_{item['internal_token']}_{st.session_state.refresh_trigger}"
                    if st.button(
                        "❌ Отклонить",
                        key=reject_key,
                        use_container_width=True
                    ):
                        if resolve_item(item['internal_token'], 'reject'):
                            st.warning("❌ Правка отклонена")
                            st.session_state.refresh_trigger += 1
                            st.rerun()
                
                with col_action3:
                    st.button("⏭️ Пропустить", key=f"skip_{item['internal_token']}", use_container_width=True)

with tabs[1]:
    st.subheader("📊 Статистика модерации")
    
    stats = get_stats()
    
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    with col_stat1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats.get('total_pending', 0)}</div>
            <div class="stat-label">На модерации</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats.get('total_approved', 0)}</div>
            <div class="stat-label">Одобрено</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats.get('total_rejected', 0)}</div>
            <div class="stat-label">Отклонено</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats.get('avg_response_time', 'N/A')}</div>
            <div class="stat-label">Среднее время</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("Coverage по категориям")
    
    if stats.get('category_coverage'):
        import pandas as pd
        df = pd.DataFrame(stats['category_coverage'])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Данные по категориям недоступны")
    
    st.markdown("---")
    
    st.subheader("Активность операторов")
    
    if stats.get('operator_activity'):
        import pandas as pd
        df = pd.DataFrame(stats['operator_activity'])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Данные по операторам недоступны")

st.sidebar.markdown("### ℹ️ Инструкция")
st.sidebar.markdown("""
**Процесс модерации:**

1. Просмотрите предложенную правку
2. Сравните старый и новый ответы
3. Используйте diff для детального анализа
4. Одобрите (✅) или отклоните (❌) правку

**После одобрения:**
- Правка применяется к базе
- Эмбеддинги обновляются автоматически
- Статистика обновляется
""")

st.sidebar.markdown("---")

st.sidebar.markdown(f"**Статус API:** {'🟢 Доступен' if True else '🔴 Недоступен'}")
st.sidebar.markdown(f"**Время:** {datetime.now().strftime('%H:%M:%S')}")
st.sidebar.markdown(f"**Правок в очереди:** {len(st.session_state.pending_items)}")

