import pandas as pd
import os
import pickle
from typing import List, Dict, Tuple
from langchain_community.document_loaders import DataFrameLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.embeddings import BGEM3Embeddings
from app.config import settings


class RAGService:
    def __init__(self):
        self.embeddings = None
        self.vector_store = None
        self.bm25_retriever = None
        self.ensemble_retriever = None
        self.llm = None
        self.df = None
        self.documents = None
        
    async def initialize(self):
        print("Инициализация RAG сервиса...")
        
        self.embeddings = BGEM3Embeddings(api_key=settings.API_KEY)
        
        self.llm = ChatOpenAI(
            api_key=settings.API_KEY,
            model=settings.LLM_MODEL,
            base_url=settings.LLM_BASE_URL,
            temperature=0.3
        )
        
        os.makedirs("./data", exist_ok=True)
        
        # Загружаем данные из CSV файла
        csv_path = "/home/kate/T1-hackathon/backend/data/knowledge_base_augmented2.csv"
        print(f"Загрузка базы знаний из {csv_path}...")
        
        self.df = pd.read_csv(csv_path)
        
        # Переименовываем колонки в нужный формат
        self.df = self.df.rename(columns={
            'Основная категория': 'category',
            'Подкатегория': 'subcategory',
            'Пример вопроса': 'question',
            'Шаблонный ответ': 'answer',
            'Целевая аудитория': 'target_group'
        })
        
        # Удаляем пустые строки
        self.df = self.df.dropna(subset=['question', 'answer'])
        
        print(f"Загружено {len(self.df)} записей из базы знаний")
        print("Создание индексов...")
        await self._build_indices()
        
        retriever = self.vector_store.as_retriever(search_kwargs={"k": settings.TOP_K})
        self.bm25_retriever.k = settings.TOP_K
        
        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[self.bm25_retriever, retriever],
            weights=[settings.BM25_WEIGHT, settings.VECTOR_WEIGHT]
        )
        
        print("RAG сервис инициализирован успешно!")
    
    async def _build_indices(self):
        loader = DataFrameLoader(self.df, page_content_column='answer')
        documents = loader.load()
        
        for i, doc in enumerate(documents):
            if i < len(self.df):
                row = self.df.iloc[i]
                doc.metadata = {
                    'category': row.get('category', ''),
                    'subcategory': row.get('subcategory', ''),
                    'question': row.get('question', ''),
                    'target_group': row.get('target_group', ''),
                }
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        self.documents = splitter.split_documents(documents)
        
        print(f"Создание эмбеддингов для {len(self.documents)} документов...")
        self.vector_store = FAISS.from_documents(self.documents, self.embeddings)
        
        print("Создание BM25 индекса...")
        self.bm25_retriever = BM25Retriever.from_documents(self.documents)
        
        print("Индексы созданы!")
    
    async def search(self, query: str, top_k: int = 3) -> Dict:
        docs = self.ensemble_retriever.get_relevant_documents(query)[:top_k]
        
        results_meta = []
        contexts = []
        
        for doc in docs:
            meta = doc.metadata
            results_meta.append({
                'question': meta.get('question', ''),
                'answer': doc.page_content,
                'taxonomy': {
                    'category': meta.get('category', ''),
                    'subcategory': meta.get('subcategory', ''),
                    'subtopic': ''
                },
                'updated_at': None
            })
            contexts.append(doc.page_content)
        
        # Возвращаем шаблонный ответ напрямую из базы знаний (без LLM)
        if contexts:
            draft = contexts[0]  # Лучший найденный ответ
        else:
            draft = "К сожалению, я не нашёл подходящей информации для ответа на этот вопрос. Пожалуйста, обратитесь в контакт-центр банка по телефону 250 или +375 (17/29/33) 309 15 15."
        
        alternatives = contexts[:3] if len(contexts) > 0 else []
        
        return {
            'draft': draft,
            'alternatives': alternatives,
            'results_meta': results_meta,
            'internal_token': None
        }
    
    async def _generate_answer(self, question: str, contexts: List[str]) -> str:
        if not contexts:
            return "К сожалению, я не нашёл подходящей информации для ответа на этот вопрос. Пожалуйста, обратитесь в контакт-центр."
        
        context_text = "\n\n".join(contexts)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Ты - помощник службы поддержки банка ВТБ (Беларусь). Твоя задача - давать точные, ясные и вежливые ответы на вопросы клиентов на основе предоставленной информации из базы знаний."),
            ("user", f"""На основе следующей информации из базы знаний:

{context_text}

Ответь на вопрос клиента: {question}

Требования к ответу:
- Будь конкретным и по делу
- Используй только информацию из контекста
- Если информации недостаточно, предложи обратиться в контакт-центр
- Сохраняй профессиональный и дружелюбный тон
- Не придумывай информацию
""")
        ])
        
        chain = prompt | self.llm
        
        try:
            response = await chain.ainvoke({
                "context": context_text,
                "question": question
            })
            return response.content
        except Exception as e:
            print(f"Ошибка генерации ответа: {e}")
            return contexts[0] if contexts else "Произошла ошибка при генерации ответа."
    
    async def save_knowledge_base(self):
        csv_path = "/home/kate/T1-hackathon/backend/data/knowledge_base_augmented2.csv"
        print(f"Сохранение базы знаний в {csv_path}...")
        
        save_df = self.df.rename(columns={
            'category': 'Основная категория',
            'subcategory': 'Подкатегория',
            'question': 'Пример вопроса',
            'answer': 'Шаблонный ответ',
            'target_group': 'Целевая аудитория'
        })
        
        save_df.to_csv(csv_path, index=False)
        print("База знаний сохранена!")
    
    async def rebuild_index_for_item(self, question: str, new_answer: str, taxonomy: Dict):
        print(f"Обновление индекса для вопроса: {question}")
        
        mask = self.df['question'] == question
        if mask.any():
            self.df.loc[mask, 'answer'] = new_answer
            if taxonomy:
                if 'category' in taxonomy:
                    self.df.loc[mask, 'category'] = taxonomy['category']
                if 'subcategory' in taxonomy:
                    self.df.loc[mask, 'subcategory'] = taxonomy['subcategory']
        else:
            new_row = {
                'category': taxonomy.get('category', ''),
                'subcategory': taxonomy.get('subcategory', ''),
                'question': question,
                'target_group': 'все клиенты',
                'answer': new_answer,
                'is_original': False
            }
            self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        
        await self._build_indices()
        
        retriever = self.vector_store.as_retriever(search_kwargs={"k": settings.TOP_K})
        self.bm25_retriever.k = settings.TOP_K
        
        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[self.bm25_retriever, retriever],
            weights=[settings.BM25_WEIGHT, settings.VECTOR_WEIGHT]
        )
        
        await self.save_knowledge_base()
        
        print("Индекс обновлён!")


rag_service = RAGService()

